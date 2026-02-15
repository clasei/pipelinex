import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import SidebarLeft from './components/SidebarLeft';
import SidebarRight from './components/SidebarRight';
import ChatInterface from './components/ChatInterface';
import Terminal from './components/Terminal';
import { INITIAL_PARAMS, INITIAL_MESSAGES, MOCK_LOGS } from './constants';
import { HyperParameters, LogEntry, ChatMessage, TrainingStats } from './types';

const API_URL = 'http://localhost:3001/api';

const App: React.FC = () => {
  const [params, setParams] = useState<HyperParameters>(INITIAL_PARAMS);
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [logs, setLogs] = useState<LogEntry[]>(MOCK_LOGS);
  const [isTraining, setIsTraining] = useState(false);
  const [isTerminalOpen, setIsTerminalOpen] = useState(true);
  
  const [stats, setStats] = useState<TrainingStats>({
    epoch: 0,
    totalEpochs: 10,
    step: 0,
    totalSteps: 10000,
    loss: 0.0,
    perplexity: 1.0,
    throughput: 0
  });

  // start training
  const startTraining = async () => {
    try {
      const response = await fetch(`${API_URL}/training/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data_path: './training_data.jsonl',
          params: {
            learning_rate: parseFloat(params.learningRate),
            batch_size: params.batchSize,
            epochs: params.epochs,
            temperature: params.temperature,
            top_p: params.topP
          }
        })
      });

      const data = await response.json();

      if (data.error) {
        addLog('ERROR', `failed to start training: ${data.error}`);
      } else {
        setIsTraining(true);
        addLog('INFO', 'training started successfully');
        addLog('INFO', `config: lr=${params.learningRate}, batch=${params.batchSize}, epochs=${params.epochs}`);
      }
    } catch (error) {
      addLog('ERROR', `connection failed: ${error}`);
    }
  };

  // stop training
  const stopTraining = async () => {
    try {
      await fetch(`${API_URL}/training/stop`, { method: 'POST' });
      setIsTraining(false);
      addLog('WARN', 'training stopped by user');
    } catch (error) {
      addLog('ERROR', `failed to stop: ${error}`);
    }
  };

  // save checkpoint
  const saveCheckpoint = async () => {
    try {
      const response = await fetch(`${API_URL}/training/checkpoint`, { method: 'POST' });
      const data = await response.json();
      addLog('PROGRESS', `checkpoint saved: ${data.path || 'checkpoint_' + Date.now()}`);
    } catch (error) {
      addLog('ERROR', `failed to save checkpoint: ${error}`);
    }
  };

  // log counter to ensure unique IDs
  const logCounterRef = useRef(0);

  // helper to add logs
  const addLog = (level: 'ERROR' | 'INFO' | 'WARN' | 'PROGRESS', message: string) => {
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];
    logCounterRef.current += 1;
    const newLog: LogEntry = {
      id: `${Date.now()}-${logCounterRef.current}`,
      timestamp: timeStr,
      level,
      message
    };
    setLogs(prev => [...prev.slice(-50), newLog]);
  };

  // poll training status
  useEffect(() => {
    if (!isTraining) return;

    let hasLoggedCompletion = false;

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/training/status`);
        const data = await response.json();

        if (data.is_training !== undefined && !data.is_training) {
          setIsTraining(false);
          if (!hasLoggedCompletion) {
            addLog('INFO', 'training completed');
            hasLoggedCompletion = true;
          }
        }

        // update stats if available
        if (data.metrics) {
          setStats({
            epoch: data.metrics.epoch || 0,
            totalEpochs: params.epochs,
            step: data.metrics.step || 0,
            totalSteps: data.metrics.total_steps || 72,
            loss: data.metrics.loss || 0,
            perplexity: Math.exp(data.metrics.loss || 0),
            throughput: data.metrics.throughput || 0
          });
        }
      } catch (error) {
        console.error('status poll failed:', error);
      }
    }, 5000); // Poll every 5 seconds (training steps take ~5s each anyway)

    return () => clearInterval(interval);
  }, [isTraining, params.epochs]);

  const handleSendMessage = async (text: string) => {
    const newUserMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: text
    };
    setMessages(prev => [...prev, newUserMsg]);

    // Show typing indicator
    const typingMsg: ChatMessage = {
      id: 'typing',
      role: 'assistant',
      text: '...'
    };
    setMessages(prev => [...prev, typingMsg]);

    try {
      // Call real API
      const response = await fetch(`${API_URL}/chat/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          model: 'mistral:latest'
        })
      });

      const data = await response.json();

      // Remove typing indicator and add real response
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== 'typing');
        return [...filtered, {
          id: Date.now().toString(),
          role: 'assistant',
          text: data.response
        }];
      });

    } catch (error) {
      console.error('chat error:', error);
      // Remove typing indicator and show error
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== 'typing');
        return [...filtered, {
          id: Date.now().toString(),
          role: 'assistant',
          text: 'Sorry, I encountered an error. Make sure the backend and Ollama are running.'
        }];
      });
    }
  };

  const handleToggleTerminal = () => setIsTerminalOpen(!isTerminalOpen);

  return (
    <div className="relative flex h-screen w-full flex-col overflow-hidden bg-background-dark">
      <Header />
      
      <main className="flex flex-1 overflow-hidden">
        <SidebarLeft />
        
        <div className="flex-1 flex flex-col min-w-0 bg-background-dark relative">
          <ChatInterface 
            messages={messages}
            isTraining={isTraining}
            stats={stats}
            onStop={() => isTraining ? stopTraining() : startTraining()}
            onCheckpoint={saveCheckpoint}
            onSendMessage={handleSendMessage}
          />
          
          <Terminal 
            logs={logs} 
            throughput={stats.throughput}
            isOpen={isTerminalOpen}
            onToggle={handleToggleTerminal}
          />
        </div>

        <SidebarRight 
          params={params} 
          setParams={setParams} 
          onApply={() => {
            addLog('WARN', 'hyperparameters updated');
          }}
        />
      </main>
    </div>
  );
};

export default App;
