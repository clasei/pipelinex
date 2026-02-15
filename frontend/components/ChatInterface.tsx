import React, { useRef, useEffect } from 'react';
import { ChatMessage, TrainingStats } from '../types';
import TrainingCard from './TrainingCard';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  isTraining: boolean;
  stats: TrainingStats;
  onStop: () => void;
  onCheckpoint: () => void;
  onSendMessage: (text: string) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  messages, 
  isTraining, 
  stats, 
  onStop, 
  onCheckpoint,
  onSendMessage
}) => {
  const [inputValue, setInputValue] = React.useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 flex flex-col min-h-0">
      <div className="flex-1 overflow-y-auto p-6 space-y-8 terminal-scroll">
        
        <TrainingCard 
            isTraining={isTraining}
            stats={stats}
            onStop={onStop}
            onCheckpoint={onCheckpoint}
        />

        {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'assistant' ? 'flex-row-reverse' : ''}`}>
                <div className={`size-10 rounded border flex items-center justify-center shrink-0 ${
                    msg.role === 'assistant' 
                    ? 'bg-primary border-primary text-background-dark' 
                    : 'bg-slate-800 border-slate-700 text-slate-400'
                }`}>
                    <span className="material-symbols-outlined font-bold">
                        {msg.role === 'assistant' ? 'bolt' : 'person'}
                    </span>
                </div>
                
                <div className={`max-w-2xl border p-4 rounded-xl ${
                    msg.role === 'assistant'
                    ? 'bg-primary/5 border-primary/20 rounded-tr-none text-slate-200'
                    : 'bg-surface-dark border-border-dark rounded-tl-none text-slate-300'
                }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                        {msg.text.split(' ').map((word, i) => {
                            if (word === msg.codeBlock || (msg.codeBlock && word.includes(msg.codeBlock))) {
                                return <code key={i} className="bg-primary/10 text-primary px-1 font-mono rounded text-xs mx-0.5 border border-primary/20">{word} </code>;
                            }
                            // Highlight numbers or metrics roughly
                            if (word.match(/\d+(\.\d+)?%/) || word.includes('tokens/sec')) {
                                return <span key={i} className="text-primary font-bold">{word} </span>
                            }
                            return word + ' ';
                        })}
                    </p>
                    {msg.metadata && (
                        <div className="mt-4 p-3 bg-background-dark rounded border border-border-dark font-mono text-[11px] text-primary/80">
                            {msg.metadata}
                        </div>
                    )}
                </div>
            </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-surface-dark border-t border-border-dark">
        <div className="max-w-4xl mx-auto relative">
          <textarea 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full bg-background-dark border border-border-dark rounded-xl px-4 py-3 pr-14 text-sm focus:ring-1 focus:ring-primary focus:border-primary placeholder-slate-600 resize-none overflow-hidden text-slate-200"
            placeholder="Send a command or message..."
            rows={1}
            style={{ minHeight: '46px' }}
          />
          <button 
            onClick={handleSend}
            disabled={!inputValue.trim()}
            className="absolute right-2 top-2 bottom-2 w-10 bg-primary text-background-dark rounded hover:scale-105 transition-transform disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center"
          >
            <span className="material-symbols-outlined font-bold text-[20px]">arrow_upward</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
