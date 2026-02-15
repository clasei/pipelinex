import React from 'react';

const SidebarLeft: React.FC = () => {
  return (
    <aside className="w-72 bg-surface-dark border-r border-border-dark flex flex-col shrink-0">
      <div className="p-4">
        <button className="w-full bg-primary hover:bg-primary/90 text-background-dark font-bold py-3 rounded-lg flex items-center justify-center gap-2 transition-all neon-glow text-sm tracking-widest font-display">
          <span className="material-symbols-outlined text-[20px]">play_circle</span>
          start loop
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 space-y-6 pt-2 pb-6 custom-scroll">
        <div>
          <h3 className="text-xs font-bold text-text-grey-light tracking-widest mb-3 px-1">active sets</h3>
          <div className="space-y-1">
            <div className="group flex items-center justify-between p-2.5 rounded-lg bg-primary/5 border border-primary/20 cursor-pointer">
              <div className="flex items-center gap-3 overflow-hidden">
                <span className="material-symbols-outlined text-primary text-[20px]">water_ec</span>
                <span className="text-sm font-medium truncate text-white">Llama-3-Surf-Instruct</span>
              </div>
              <span className="size-2 rounded-full bg-primary shadow-[0_0_5px_#0099dd]"></span>
            </div>
            
            {['Coder-Hack-v2', 'Mistral-Flow-7B'].map((model, idx) => (
              <div key={idx} className="group flex items-center justify-between p-2.5 rounded-lg hover:bg-white/5 border border-transparent cursor-pointer transition-all">
                <div className="flex items-center gap-3 overflow-hidden">
                  <span className="material-symbols-outlined text-slate-500 text-[20px]">terminal</span>
                  <span className="text-sm font-medium text-text-grey-light group-hover:text-white truncate">{model}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="p-4 border-t border-border-dark bg-background-dark/50">
        <div className="flex items-center justify-between text-[11px] mb-2">
          <span className="text-text-grey-light font-bold tracking-tighter">vram load</span>
          <span className="text-primary font-mono">18.4GB / 24GB</span>
        </div>
        <div className="w-full bg-border-dark h-1 rounded-full overflow-hidden">
          <div className="bg-primary h-full w-[76%] shadow-[0_0_8px_#0099dd]"></div>
        </div>
      </div>
    </aside>
  );
};

export default SidebarLeft;