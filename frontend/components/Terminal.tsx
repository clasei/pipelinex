import React, { useEffect, useRef } from 'react';
import { LogEntry } from '../types';

interface TerminalProps {
  logs: LogEntry[];
  throughput: number;
  isOpen: boolean;
  onToggle: () => void;
}

const Terminal: React.FC<TerminalProps> = ({ logs, throughput, isOpen, onToggle }) => {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs, isOpen]);

  if (!isOpen) return (
     <div className="bg-surface-dark border-t border-border-dark px-4 py-2 flex items-center justify-between cursor-pointer hover:bg-white/5" onClick={onToggle}>
        <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-xs text-slate-400">terminal</span>
            <span className="text-[10px] font-bold text-slate-400 tracking-widest">training logs</span>
        </div>
        <span className="material-symbols-outlined text-xs text-slate-500">expand_less</span>
     </div>
  );

  return (
    <div className="h-64 border-t border-border-dark bg-black/40 flex flex-col shrink-0 transition-all duration-300">
      <div className="flex items-center justify-between px-4 py-2 bg-surface-dark border-b border-border-dark">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 cursor-pointer" onClick={onToggle}>
            <span className="material-symbols-outlined text-xs text-slate-400">terminal</span>
            <span className="text-[10px] font-bold text-slate-400 tracking-widest">training logs</span>
          </div>
          <div className="flex items-center gap-2 border-l border-border-dark pl-4">
            <span className="text-[10px] text-slate-500 font-mono">throughput:</span>
            <span className="text-[10px] text-primary font-mono font-bold">{throughput.toLocaleString()} tps</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
            <button onClick={onToggle} className="hover:text-white text-slate-500 flex items-center">
                 <span className="material-symbols-outlined text-xs">close_fullscreen</span>
            </button>
        </div>
      </div>
      
      <div className="flex-1 p-4 font-mono text-[11px] text-slate-400 overflow-y-auto terminal-scroll bg-black/20">
        {logs.map((log) => (
          <div key={log.id} className="mb-1 leading-relaxed break-words hover:bg-white/5 px-1 -mx-1 rounded">
            <span className="text-slate-500 select-none">[{log.timestamp}]</span>{' '}
            {log.level === 'INFO' && <span className="text-primary font-bold">INFO:</span>}
            {log.level === 'WARN' && <span className="text-yellow-500/90 font-bold">WARN:</span>}
            {log.level === 'ERROR' && <span className="text-red-500 font-bold">ERROR:</span>}
            {log.level === 'PROGRESS' && <span className="text-primary font-bold">PROGRESS:</span>}
            {' '}
            <span className={log.level === 'WARN' ? 'text-yellow-500/80' : log.level === 'PROGRESS' ? 'text-primary' : 'text-slate-400'}>
              {log.message}
            </span>
          </div>
        ))}
        <div className="text-primary animate-pulse font-bold mt-1">_</div>
        <div ref={endRef} />
      </div>
    </div>
  );
};

export default Terminal;
