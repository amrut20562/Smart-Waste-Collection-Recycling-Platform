import React from 'react';
import { AlertTriangle, Trash2, Recycle } from 'lucide-react';
import type { DisposalInfo } from '../types';

interface DisposalCardProps {
  category: string;
  displayName: string;
  disposal: DisposalInfo;
}

export const DisposalCard: React.FC<DisposalCardProps> = ({ category, displayName, disposal }) => {
  const getStreamBadgeColor = (stream: string) => {
    if (stream.includes('Recyclable')) return 'bg-eco-500/20 text-eco-300 border border-eco-500/30';
    if (stream.includes('Organic')) return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
    if (stream.includes('Hazardous') || stream.includes('E-Waste')) return 'bg-rose-500/20 text-rose-300 border border-rose-500/30';
    return 'bg-zinc-500/20 text-zinc-300 border border-zinc-500/30';
  };

  return (
    <div className="card border-l-4 border-eco-500 bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-xl">
      <div className="flex items-start gap-3 mb-4">
        <div className="p-2.5 rounded-xl bg-eco-500/20 border border-eco-500/30">
          {disposal.special_handling ? (
            <AlertTriangle className="h-6 w-6 text-amber-400" />
          ) : disposal.waste_stream.includes('Recyclable') ? (
            <Recycle className="h-6 w-6 text-eco-400" />
          ) : (
            <Trash2 className="h-6 w-6 text-eco-400" />
          )}
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white mb-1">{displayName}</h3>
          <span className={`badge ${getStreamBadgeColor(disposal.waste_stream)}`}>
            {disposal.waste_stream}
          </span>
        </div>
      </div>

      {disposal.warning && (
        <div className="mb-4 p-3 bg-amber-950/40 border-l-4 border-amber-500 border border-amber-500/30 rounded-xl">
          <div className="flex items-start gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-amber-200 font-medium">{disposal.warning}</p>
          </div>
        </div>
      )}

      <div>
        <h4 className="text-sm font-semibold text-white mb-2">Disposal Instructions:</h4>
        <ul className="space-y-2">
          {disposal.instructions.map((instruction, idx) => (
            <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
              <span className="text-eco-400 font-bold flex-shrink-0">•</span>
              <span>{instruction}</span>
            </li>
          ))}
        </ul>
      </div>

      {disposal.special_handling && (
        <div className="mt-4 flex items-center gap-2 text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20 rounded-lg p-2">
          <AlertTriangle className="h-4 w-4" />
          <span className="font-medium">Special handling required</span>
        </div>
      )}
    </div>
  );
};
