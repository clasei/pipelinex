import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="flex items-center justify-between border-b border-border-subtle bg-surface-dark px-6 py-3 h-16 shrink-0 z-10">
      <div className="flex items-center gap-8">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center size-8 rounded bg-primary/10 text-primary">
            <span className="material-symbols-outlined font-bold text-[18px]">waves</span>
          </div>
          <h1 className="text-lg font-medium tracking-tight font-display">
            <span className="text-gray-100">pipeline</span><span className="text-primary">x</span>
          </h1>
        </div>
        
        <nav className="hidden md:flex items-center gap-6">
          <a href="#" className="text-primary text-sm font-medium tracking-wide border-b-2 border-primary pb-0">flow</a>
          <a href="https://github.com/clasei/pipelinex/tree/develop/docs" target="_blank" rel="noopener noreferrer" className="text-text-grey-light hover:text-primary text-sm font-medium transition-colors border-b-2 border-transparent pb-0">docs</a>
        </nav>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-surface-darker border border-border-subtle rounded text-xs font-mono">
          <span className="size-1.5 rounded-full bg-primary animate-pulse"></span>
          <span className="text-text-grey-light">active</span>
          <span className="text-primary font-medium">live</span>
        </div>
      </div>
    </header>
  );
};

export default Header;