import React from 'react';

export const AmmachiMascot = ({ size = 'md', className = '', speaking = false }) => {
  const sizeClasses = {
    sm: 'w-12 h-12 text-2xl',
    md: 'w-16 h-16 text-3xl',
    lg: 'w-24 h-24 text-5xl',
    xl: 'w-32 h-32 text-6xl'
  };

  return (
    <div className={`relative inline-flex items-center justify-center rounded-full bg-gradient-to-tr from-amber-400 to-orange-400 p-1 shadow-md ${speaking ? 'ring-4 ring-amber-300 animate-pulse' : ''} ${className}`}>
      <div className={`flex items-center justify-center rounded-full bg-amber-50 shadow-inner ${sizeClasses[size] || sizeClasses.md}`}>
        <span role="img" aria-label="Ammachi Mascot" className="select-none transform hover:scale-110 transition-transform">
          👵
        </span>
      </div>
      {speaking && (
        <span className="absolute -top-1 -right-1 flex h-4 w-4">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-4 w-4 bg-orange-500"></span>
        </span>
      )}
    </div>
  );
};
