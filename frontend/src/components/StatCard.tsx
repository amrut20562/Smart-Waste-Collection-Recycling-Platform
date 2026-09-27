import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  color?: string;
}

export const StatCard: React.FC<StatCardProps> = ({ title, value, icon: Icon, color = 'eco-400' }) => {
  const getIconColorClass = (c: string) => {
    if (c.includes('red')) return 'text-rose-400 bg-rose-500/15 border-rose-500/30';
    if (c.includes('blue')) return 'text-sky-400 bg-sky-500/15 border-sky-500/30';
    if (c.includes('green')) return 'text-emerald-400 bg-emerald-500/15 border-emerald-500/30';
    return 'text-eco-400 bg-eco-500/15 border-eco-500/30';
  };

  return (
    <div className="card bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-lg hover:border-white/20 transition-all">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-300 mb-1">{title}</p>
          <p className="text-3xl font-extrabold text-white tracking-tight">{value}</p>
        </div>
        <div className={`p-3 rounded-xl border ${getIconColorClass(color)}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
};
