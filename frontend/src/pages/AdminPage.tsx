import React, { useState, useEffect } from 'react';
import { ArrowLeft, Package, AlertCircle, Truck, CheckCircle2, TrendingDown, Map as MapIcon, Loader2, BarChart3, Layers } from 'lucide-react';
import { Link } from 'react-router-dom';
import { StatCard } from '../components/StatCard';
import { RequestTable } from '../components/RequestTable';
import { OperationsMap } from '../components/OperationsMap';
import { RouteResults } from '../components/RouteResults';
import { api } from '../api/client';
import type { AdminOverview, PickupRequest, Vehicle, ClusterItem, RouteOptimizeResponse } from '../types';
import ShaderAuroraVeil from '../components/ui/shader-aurora-veil';

export const AdminPage: React.FC = () => {
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [requests, setRequests] = useState<PickupRequest[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [clusters, setClusters] = useState<ClusterItem[]>([]);
  const [routeResult, setRouteResult] = useState<RouteOptimizeResponse | null>(null);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [isClustering, setIsClustering] = useState(false);

  const loadData = async () => {
    try {
      const [overviewData, allRequests, vehicleData] = await Promise.all([
        api.getAdminOverview(),
        api.getPickups(),
        api.getVehicles(),
      ]);
      setOverview(overviewData);
      setRequests(allRequests);
      setVehicles(vehicleData);
    } catch (err) {
      console.error('Failed to load admin data:', err);
    }
  };

  useEffect(() => { loadData(); }, []);

  const handleFindClusters = async () => {
    setIsClustering(true);
    try {
      const clusterData = await api.getClusters();
      setClusters(clusterData);
    } catch { alert('Failed to generate clusters'); }
    finally { setIsClustering(false); }
  };

  const handleOptimizeRoutes = async () => {
    const pending = requests.filter(r => r.status === 'PENDING');
    const active = vehicles.filter(v => v.active);
    if (pending.length === 0) { alert('No pending requests'); return; }
    if (active.length === 0) { alert('No active vehicles'); return; }
    setIsOptimizing(true);
    try {
      const result = await api.optimizeRoutes(active.map(v => v.id), pending.map(r => r.id));
      setRouteResult(result);
      await loadData();
    } catch (err: any) { alert(err.message || 'Optimization failed'); }
    finally { setIsOptimizing(false); }
  };

  const handleReset = async () => {
    try {
      await api.resetDemo();
      await loadData();
      alert('Demo data reset successfully');
    } catch (err: any) {
      alert('Failed to reset demo: ' + err.message);
    }
  };

  const pending = requests.filter(r => r.status === 'PENDING');
  const highPriority = pending.filter(r => r.priority_score >= 70);

  return (
    <div className="relative min-h-screen bg-[#0a0a0f]">
      {/* Aurora veil background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <ShaderAuroraVeil preset="aurora-veil" tone="dark" className="h-full w-full" />
      </div>

      <header className="relative z-10 bg-[#12121a]/80 backdrop-blur-sm shadow-[0_2px_8px_rgb(0,0,0,0.3)] border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 md:px-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link to="/" className="text-gray-400 hover:text-white transition-colors">
                <ArrowLeft className="h-6 w-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white tracking-tight">Operations Command Center</h1>
                <p className="text-sm text-gray-300">Real-time collection management and optimization</p>
              </div>
            </div>
            <button onClick={handleReset} className="btn-secondary text-sm">
              Reset Demo
            </button>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-6 py-8 md:px-12 space-y-8">
        {/* KPI Cards - 4-column grid */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard title="Pending Requests" value={overview.pending} icon={Package} />
            <StatCard title="High Priority" value={overview.high_priority} icon={AlertCircle} color="red-600" />
            <StatCard title="Active Vehicles" value={overview.active_vehicles} icon={Truck} color="blue-600" />
            <StatCard title="Completed Today" value={overview.completed} icon={CheckCircle2} color="green-600" />
          </div>
        )}

        {/* Main Action Grid - Asymmetric */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <OperationsMap requests={pending} clusters={clusters} vehicles={vehicles} />
          </div>
          <div className="space-y-4">
            <div className="card">
              <h3 className="text-lg font-bold text-white mb-4">Cluster & Route Actions</h3>
              <button
                onClick={handleFindClusters}
                disabled={isClustering || pending.length === 0}
                className="btn-secondary w-full mb-3 flex items-center justify-center gap-2"
              >
                {isClustering ? <><Loader2 className="h-5 w-5 animate-spin" /> Finding... </> : <><MapIcon className="h-5 w-5" /> Find Clusters</>}
              </button>
              <button
                onClick={handleOptimizeRoutes}
                disabled={isOptimizing || pending.length === 0}
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                {isOptimizing ? <><Loader2 className="h-5 w-5 animate-spin" /> Optimizing... </> : <><TrendingDown className="h-5 w-5" /> Optimize Routes</>}
              </button>
              {clusters.length > 0 && (
                <div className="mt-4 p-3 bg-eco-950/40 rounded-xl border border-eco-500/30">
                  <p className="text-sm text-eco-300"><strong>{clusters.length}</strong> geographic clusters identified</p>
                </div>
              )}
            </div>

            {highPriority.length > 0 && (
              <div className="card border-l-4 border-red-500">
                <h3 className="text-lg font-bold text-white mb-3">High Priority Queue</h3>
                <div className="space-y-2">
                  {highPriority.slice(0, 5).map(req => (
                    <div key={req.id} className="p-2.5 bg-red-950/30 border border-red-500/25 rounded-lg">
                      <div className="font-semibold text-sm text-white">Pickup #{req.id} — {req.waste_category?.replace('_', ' ')}</div>
                      <div className="text-xs text-red-400">Priority: {req.priority_score?.toFixed(1)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Route Results Modal */}
        {routeResult && (
          <div className="animate-fadeIn">
            <RouteResults result={routeResult} requests={requests} />
          </div>
        )}

        {/* Request Table */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Layers className="h-5 w-5 text-eco-400" />
            <h2 className="text-xl font-bold text-white">All Pickup Requests</h2>
          </div>
          <RequestTable requests={requests} />
        </div>
      </main>
    </div>
  );
};