import React from 'react';
import { HyperParameters } from '../types';

interface SidebarRightProps {
  params: HyperParameters;
  setParams: React.Dispatch<React.SetStateAction<HyperParameters>>;
  onApply: () => void;
}

const SidebarRight: React.FC<SidebarRightProps> = ({ params, setParams, onApply }) => {
  
  const handleChange = (key: keyof HyperParameters, value: any) => {
    setParams(prev => ({ ...prev, [key]: value }));
  };

  return (
    <aside className="w-80 bg-surface-dark border-l border-border-dark flex flex-col shrink-0">
      <div className="p-4 border-b border-border-dark flex items-center justify-between bg-white/5 border-b border-white/10">
        <h2 className="text-sm font-bold tracking-widest text-white">hyperparameters</h2>
        <span className="material-symbols-outlined text-slate-500 text-sm">settings_input_component</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-8 terminal-scroll">
        {/* Sampling Config */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-text-grey-light tracking-tighter">sampling config</span>
            <span className="text-[10px] text-text-grey">profiles: default</span>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <label className="text-xs font-medium text-text-grey-light">Temperature</label>
                <span className="text-xs font-mono text-primary">{params.temperature.toFixed(2)}</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="2" 
                step="0.05" 
                value={params.temperature}
                onChange={(e) => handleChange('temperature', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-background-dark rounded-lg appearance-none cursor-pointer custom-range"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <label className="text-xs font-medium text-text-grey-light">Top-P (Nucleus)</label>
                <span className="text-xs font-mono text-primary">{params.topP.toFixed(2)}</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01" 
                value={params.topP}
                onChange={(e) => handleChange('topP', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-background-dark rounded-lg appearance-none cursor-pointer custom-range"
              />
            </div>
          </div>
        </div>

        {/* Trainer Engine */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-text-grey-light tracking-tighter">trainer engine</span>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <label className="text-xs font-medium text-text-grey-light">Learning Rate</label>
                <span className="text-xs font-mono text-primary">{params.learningRate}</span>
              </div>
              <div className="grid grid-cols-4 gap-2">
                {['1e-5', '5e-5', '1e-4', '5e-4'].map((rate) => (
                  <button
                    key={rate}
                    onClick={() => handleChange('learningRate', rate)}
                    className={`px-2 py-1.5 text-[10px] font-mono text-center rounded transition-all ${
                      params.learningRate === rate 
                        ? 'bg-primary/20 border border-primary text-primary' 
                        : 'bg-background-dark border border-border-dark text-text-grey hover:border-primary/50'
                    }`}
                  >
                    {rate}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <label className="text-xs font-medium text-text-grey-light">Batch Size</label>
                <span className="text-xs font-mono text-primary">{params.batchSize}</span>
              </div>
              <div className="flex items-center gap-3">
                <input 
                  type="number" 
                  value={params.batchSize}
                  onChange={(e) => handleChange('batchSize', parseInt(e.target.value) || 0)}
                  className="flex-1 bg-background-dark border border-border-dark rounded px-3 py-1.5 text-xs font-mono text-primary focus:ring-1 focus:ring-primary focus:border-primary outline-none"
                />
                <span className="text-[10px] text-text-grey font-mono">steps/acc</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <label className="text-xs font-medium text-text-grey-light">Epochs</label>
                <span className="text-xs font-mono text-primary">{params.epochs}</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="50" 
                step="1" 
                value={params.epochs}
                onChange={(e) => handleChange('epochs', parseInt(e.target.value))}
                className="w-full h-1.5 bg-background-dark rounded-lg appearance-none cursor-pointer custom-range"
              />
            </div>

            <div className="pt-4 space-y-3">
              <button 
                onClick={() => handleChange('useLoRA', !params.useLoRA)}
                className={`w-full flex items-center justify-between px-3 py-2 border rounded-lg transition-all ${
                  params.useLoRA ? 'bg-background-dark border-border-dark' : 'bg-background-dark border-border-dark opacity-75'
                }`}
              >
                <span className="text-xs text-text-grey-light font-medium">Use LoRA</span>
                <div className={`w-8 h-4 rounded-full relative transition-colors ${
                  params.useLoRA ? 'bg-primary/20 border border-primary/40' : 'bg-slate-800'
                }`}>
                  <div className={`absolute top-0.5 size-3 rounded-full transition-all ${
                    params.useLoRA ? 'left-[18px] bg-primary' : 'left-0.5 bg-slate-600'
                  }`}></div>
                </div>
              </button>

              <button 
                onClick={() => handleChange('quantization', !params.quantization)}
                className={`w-full flex items-center justify-between px-3 py-2 border rounded-lg transition-all ${
                  params.quantization ? 'bg-background-dark border-border-dark' : 'bg-background-dark border-border-dark opacity-50'
                }`}
              >
                <span className="text-xs text-text-grey-light font-medium">Quantization (4-bit)</span>
                <div className={`w-8 h-4 rounded-full relative transition-colors ${
                  params.quantization ? 'bg-primary/20 border border-primary/40' : 'bg-slate-800'
                }`}>
                  <div className={`absolute top-0.5 size-3 rounded-full transition-all ${
                    params.quantization ? 'left-[18px] bg-primary' : 'left-0.5 bg-slate-600'
                  }`}></div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 border-t border-border-dark bg-background-dark/30">
        <button 
            onClick={onApply}
            className="w-full bg-white/5 border border-white/10 text-white hover:bg-white/10 hover:border-primary text-xs font-bold py-3 rounded-lg transition-all tracking-widest"
        >
            apply parameters
        </button>
      </div>
    </aside>
  );
};

export default SidebarRight;
