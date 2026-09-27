import React, { useState, useEffect } from 'react';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { WasteScanner } from '../components/WasteScanner';
import { PickupForm } from '../components/PickupForm';
import { RequestTable } from '../components/RequestTable';
import { api } from '../api/client';
import type { VisionResult, PickupRequest } from '../types';
import ShaderAuroraVeil from '../components/ui/shader-aurora-veil';

export const CitizenPage: React.FC = () => {
  const [scanResult, setScanResult] = useState<VisionResult | null>(null);
  const [showPickupForm, setShowPickupForm] = useState(false);
  const [myRequests, setMyRequests] = useState<PickupRequest[]>([]);

  const loadMyRequests = async () => {
    try {
      const all = await api.getPickups();
      // Filter by user_id = 2 (default citizen)
      setMyRequests(all.filter(r => r.user_id === 2));
    } catch (err) {
      console.error('Failed to load requests:', err);
    }
  };

  useEffect(() => {
    loadMyRequests();
  }, []);

  const handleScanComplete = (result: VisionResult) => {
    setScanResult(result);
    setShowPickupForm(true);
  };

  const handlePickupSuccess = () => {
    setShowPickupForm(false);
    setScanResult(null);
    loadMyRequests();
  };

  return (
    <div className="relative min-h-screen bg-[#0a0a0f]">
      {/* Aurora veil background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <ShaderAuroraVeil preset="aurora-veil" tone="dark" className="h-full w-full" />
      </div>

      <header className="relative z-10 bg-[#12121a]/80 backdrop-blur-sm shadow-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link to="/" className="text-gray-400 hover:text-white transition-colors">
                <ArrowLeft className="h-6 w-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white">Citizen Portal</h1>
                <p className="text-sm text-gray-300">Scan waste · Get guidance · Request pickup</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-6">
            <WasteScanner onScanComplete={handleScanComplete} />
          </div>

          <div className="space-y-6">
            {showPickupForm && (
              <PickupForm scanResult={scanResult || undefined} onSuccess={handlePickupSuccess} />
            )}

            {!showPickupForm && scanResult && (
              <div className="card bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-xl">
                <h3 className="text-lg font-bold mb-3 text-white">Next Step</h3>
                <p className="text-gray-200 mb-4">
                  Your waste has been identified. Would you like to request a pickup?
                </p>
                <button onClick={() => setShowPickupForm(true)} className="btn-primary w-full">
                  Request Pickup
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-bold text-white mb-4">My Pickup Requests</h2>
          <RequestTable requests={myRequests} />
        </div>
      </main>
    </div>
  );
};
