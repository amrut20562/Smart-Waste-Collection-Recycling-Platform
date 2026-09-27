import React from 'react';
import { Truck, Package, MapPin, TrendingDown, CheckCircle2 } from 'lucide-react';
import type { RouteOptimizeResponse, PickupRequest } from '../types';

interface RouteResultsProps {
  result: RouteOptimizeResponse;
  requests: PickupRequest[];
}

export const RouteResults: React.FC<RouteResultsProps> = ({ result, requests }) => {
  const getRequestById = (id: number) => requests.find(r => r.id === id);

  return (
    <div className="space-y-4">
      {/* Metrics Summary */}
      <div className="card bg-[#12121a]/85 backdrop-blur-md border-l-4 border-eco-500 border border-white/10 shadow-xl">
        <div className="flex items-center gap-3 mb-4">
          <CheckCircle2 className="h-8 w-8 text-eco-400" />
          <div>
            <h3 className="text-lg font-bold text-white">Route Optimization Complete</h3>
            <p className="text-sm text-gray-300">Status: {result.solver_status}</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-4">
          <div className="text-center p-3.5 bg-white/[0.04] border border-white/10 rounded-xl">
            <p className="text-xs text-gray-300 mb-1">Baseline Distance</p>
            <p className="text-2xl font-bold text-white">
              {result.metrics.baseline_distance_km.toFixed(1)} km
            </p>
          </div>
          <div className="text-center p-3.5 bg-white/[0.04] border border-white/10 rounded-xl">
            <p className="text-xs text-gray-300 mb-1">Optimized Distance</p>
            <p className="text-2xl font-bold text-eco-400">
              {result.metrics.optimized_distance_km.toFixed(1)} km
            </p>
          </div>
          <div className="text-center p-3.5 bg-eco-500 text-white rounded-xl shadow-lg shadow-eco-500/25">
            <div className="flex items-center justify-center gap-1 mb-1">
              <TrendingDown className="h-4 w-4" />
              <p className="text-xs font-medium">Distance Saved</p>
            </div>
            <p className="text-2xl font-extrabold">
              {result.metrics.estimated_reduction_pct.toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      {/* Vehicle Routes */}
      <div className="space-y-3">
        <h3 className="text-lg font-bold text-white">Vehicle Routes ({result.vehicles.length})</h3>
        {result.vehicles.map((vehicle) => {
          const hasStops = vehicle.stops && vehicle.stops.length > 0;

          return (
            <div key={vehicle.vehicle_id} className="card border-l-4 border-blue-500 bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-lg">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-blue-500/20 border border-blue-500/30">
                    <Truck className="h-6 w-6 text-blue-400" />
                  </div>
                  <div>
                    <h4 className="font-bold text-white">Vehicle #{vehicle.vehicle_id}</h4>
                    <p className="text-sm text-gray-300">
                      {hasStops ? `${vehicle.stops.length} stops` : 'No stops assigned'}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-300">Distance</p>
                  <p className="text-lg font-bold text-white">{vehicle.distance_km.toFixed(1)} km</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-3">
                <div className="flex items-center gap-2 text-sm text-gray-200">
                  <Package className="h-4 w-4 text-eco-400" />
                  <span>Load: <strong className="text-white">{vehicle.load_units}</strong> / {vehicle.capacity_units} units</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2 mt-2 overflow-hidden">
                  <div
                    className="bg-eco-400 h-2 rounded-full transition-all"
                    style={{ width: `${Math.min(100, (vehicle.load_units / vehicle.capacity_units) * 100)}%` }}
                  />
                </div>
              </div>

              {hasStops && (
                <div className="mt-3 border-t border-white/10 pt-3">
                  <p className="text-xs font-semibold text-white mb-2 uppercase tracking-wide">Stop Sequence:</p>
                  <div className="space-y-2">
                    {vehicle.stops.map((pickupId, stopIdx) => {
                      const req = getRequestById(pickupId);
                      return (
                        <div key={stopIdx} className="flex items-center gap-2 text-sm p-2 rounded-lg bg-white/[0.02] border border-white/5">
                          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold shadow-md">
                            {stopIdx + 1}
                          </div>
                          <MapPin className="h-4 w-4 text-gray-400" />
                          <span className="text-white font-medium">
                            Pickup #{pickupId}
                            {req && (
                              <span className="text-gray-300 ml-2 capitalize font-normal">
                                ({req.waste_category.replace('_', ' ')}, {req.load_units} units)
                              </span>
                            )}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
