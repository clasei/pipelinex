import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import SidebarLeft from './components/SidebarLeft';
import SidebarRight from './components/SidebarRight';
import ChatInterface from './components/ChatInterface';
import Terminal from './components/Terminal';
import { INITIAL_PARAMS, INITIAL_MESSAGES, MOCK_LOGS } from './constants';
import { HyperParameters, LogEntry, ChatMessage, TrainingStats } from './types';

const App: React.FC = () => {
  const [params, setParams] = useState<HyperParameters>(INITIAL_PARAMS);
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [logs, setLogs] = useState<LogEntry[]>(MOCK_LOGS);
  const [isTraining, setIsTraining] = useState(true);
  const [isTerminalOpen, setIsTerminalOpen] = useState(true);
  
  const [stats, setStats] = useState<TrainingStats>({
    epoch: 3,
    totalEpochs: 10,
    step: 4250,
    totalSteps: 10000,
    loss: 0.0412,
    perplexity: 1.04,
    throughput: 1450
  });

  // Simulator for logs and training stats
  useEffect(() => {
    if (!isTraining) return;

    const interval = setInterval(() => {
      setStats(prev => {
        const newStep = prev.step + 5;
        const newLoss = Math.max(0.01, prev.loss - 0.0001 + (Math.random() * 0.0002 - 0.0001));
        return {
          ...prev,
          step: newStep,
          loss: newLoss,
          throughput: 1400 + Math.floor(Math.random() * 100)
        };
      });

      if (Math.random() > 0.7) {
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        const newLog: LogEntry = {
          id: Date.now().toString(),
          timestamp: timeStr,
          level: 'INFO',
          message: `Epoch 3/10 | Step ${stats.step}/10000 | Loss: ${stats.loss.toFixed(4)} | Perplexity: ${stats.perplexity.toFixed(2)}`
        };
        setLogs(prev => [...prev.slice(-50), newLog]);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isTraining, stats.step, stats.loss, stats.perplexity]);

  const handleSendMessage = (text: string) => {
    const newUserMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: text
    };
    setMessages(prev => [...prev, newUserMsg]);

    // Simulate response
    setTimeout(() => {
      const newAiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: `Acknowledged. Processing request for "${text}". No anomalies detected in current batch.`
      };
      setMessages(prev => [...prev, newAiMsg]);
    }, 1200);
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
            onStop={() => setIsTraining(!isTraining)}
            onCheckpoint={() => {
                setLogs(prev => [...prev, {
                    id: Date.now().toString(),
                    timestamp: new Date().toTimeString().split(' ')[0],
                    level: 'PROGRESS',
                    message: `Saving Checkpoint: chk_${stats.step}... Done.`
                }])
            }}
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
            setLogs(prev => [...prev, {
                id: Date.now().toString(),
                timestamp: new Date().toTimeString().split(' ')[0],
                level: 'WARN',
                message: `Hyperparameters updated. Restarting optimizer...`
            }])
          }}
        />
      </main>
    </div>
  );
};

export default App;
