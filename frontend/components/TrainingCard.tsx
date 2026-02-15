import React from 'react';
import { TrainingStats } from '../types';

interface TrainingCardProps {
  isTraining: boolean;
  stats: TrainingStats;
  onStop: () => void;
  onCheckpoint: () => void;
}

const TrainingCard: React.FC<TrainingCardProps> = ({ isTraining, stats, onStop, onCheckpoint }) => {
  return (
    <div className="flex items-center justify-between bg-surface-dark border border-border-dark rounded-xl p-4 shadow-lg shadow-black/20">
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-lg flex items-center justify-center transition-colors ${isTraining ? 'bg-primary/10 text-primary' : 'bg-slate-800 text-slate-500'}`}>
          <span className={`material-symbols-outlined ${isTraining ? 'animate-pulse' : ''}`}>analytics</span>
        </div>
        <div>
          <h2 className={`text-sm font-bold tracking-widest transition-colors ${isTraining ? 'text-primary' : 'text-slate-500'}`}>
            {isTraining ? 'training live' : 'training paused'}
          </h2>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            epoch {stats.epoch}/{stats.totalEpochs} • step {stats.step.toLocaleString()} • loss: {stats.loss.toFixed(4)}
          </p>
        </div>
      </div>
      
      <div className="flex gap-2">
        <button 
            onClick={onStop}
            className={`px-4 py-2 border rounded-lg text-xs font-bold transition-all ${
                isTraining 
                ? 'bg-red-900/20 text-red-400 border-red-600/30 hover:bg-red-900/40 hover:text-red-300'
                : 'bg-primary/10 text-primary border-primary/20 hover:bg-primary hover:text-black'
            }`}
        >
            {isTraining ? 'stop training' : 'start training'}
        </button>
        <button 
            onClick={onCheckpoint}
            className="px-4 py-2 bg-surface-dark border border-border-dark rounded-lg text-xs font-bold hover:border-primary text-slate-300 hover:text-white transition-all"
        >
            checkpoint
        </button>
      </div>
    </div>
  );
};

export default TrainingCard;
