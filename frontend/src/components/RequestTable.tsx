import React from 'react';
import { MapPin, Package, Clock } from 'lucide-react';
import type { PickupRequest, PickupStatus } from '../types';

interface RequestTableProps {
  requests: PickupRequest[];
  onSelectRequest?: (id: number) => void;
}

export const RequestTable: React.FC<RequestTableProps> = ({ requests, onSelectRequest }) => {
  const getStatusBadge = (status: PickupStatus) => {
    const styles: Record<PickupStatus, string> = {
      PENDING: 'bg-amber-500/15 text-amber-300 border border-amber-500/30',
      ASSIGNED: 'bg-blue-500/15 text-blue-300 border border-blue-500/30',
      IN_PROGRESS: 'bg-purple-500/15 text-purple-300 border border-purple-500/30',
      COMPLETED: 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30',
      CANCELLED: 'bg-zinc-500/15 text-zinc-300 border border-zinc-500/30',
    };
    return <span className={`badge ${styles[status]}`}>{status}</span>;
  };

  const getPriorityBadge = (score: number) => {
    if (score >= 70) return <span className="badge bg-rose-500/20 text-rose-300 border border-rose-500/30 font-semibold">High Priority</span>;
    if (score >= 40) return <span className="badge bg-amber-500/20 text-amber-300 border border-amber-500/30">Medium</span>;
    return <span className="badge bg-zinc-500/20 text-zinc-300 border border-zinc-500/30">Normal</span>;
  };

  return (
    <div className="card overflow-hidden bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-2xl p-0">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-white/10">
          <thead className="bg-white/[0.04]">
            <tr>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                ID
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Category
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Location
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Scheduled
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Load
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Priority
              </th>
              <th className="px-5 py-3.5 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 bg-transparent">
            {requests.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-5 py-10 text-center text-gray-400">
                  No pickup requests found
                </td>
              </tr>
            ) : (
              requests.map((req) => (
                <tr
                  key={req.id}
                  className="hover:bg-white/[0.05] cursor-pointer transition-colors"
                  onClick={() => onSelectRequest?.(req.id)}
                >
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm font-semibold text-white">
                    #{req.id}
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm font-medium text-white">
                    <span className="capitalize">{req.waste_category.replace('_', ' ')}</span>
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm text-gray-300">
                    <MapPin className="inline h-4 w-4 mr-1 text-eco-400" />
                    {req.latitude.toFixed(4)}, {req.longitude.toFixed(4)}
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm text-gray-300">
                    <Clock className="inline h-4 w-4 mr-1 text-gray-400" />
                    <span className="text-white font-medium">{req.scheduled_date}</span>
                    {req.scheduled_window && <span className="text-xs text-gray-400 ml-1.5 font-mono">({req.scheduled_window})</span>}
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm text-white font-medium">
                    <Package className="inline h-4 w-4 mr-1.5 text-eco-400" />
                    {req.load_units} <span className="text-xs text-gray-400">units</span>
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm">
                    <div className="flex items-center gap-2">
                      {getPriorityBadge(req.priority_score)}
                      <span className="text-xs font-semibold text-white">{req.priority_score.toFixed(1)}</span>
                    </div>
                  </td>
                  <td className="px-5 py-3.5 whitespace-nowrap text-sm">
                    {getStatusBadge(req.status)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
