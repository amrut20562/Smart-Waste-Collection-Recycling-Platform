import React, { useState } from 'react';
import { MapPin as MapPinIcon, Calendar, Package, FileText, CheckCircle2 } from 'lucide-react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { api } from '../api/client';
import type { VisionResult } from '../types';

// Internal component for clickable map
const MapPicker: React.FC<{ position: [number, number]; setPosition: (pos: [number, number]) => void }> = ({ position, setPosition }) => {
  useMapEvents({
    click(e) {
      setPosition([e.latlng.lat, e.latlng.lng]);
    },
  });
  return <Marker position={position} />;
};

interface PickupFormProps {
  scanResult?: VisionResult;
  onSuccess?: () => void;
}

export const PickupForm: React.FC<PickupFormProps> = ({ scanResult, onSuccess }) => {
  const [formData, setFormData] = useState({
    waste_category: scanResult?.category || 'plastic',
    latitude: 18.5204,
    longitude: 73.8567,
    scheduled_date: new Date().toISOString().split('T')[0],
    scheduled_window: '09:00-11:00',
    load_units: 3,
    description: '',
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      await api.createPickup({
        user_id: 2, // Default citizen user
        ...formData,
      });
      setSuccess(true);
      setTimeout(() => {
        if (onSuccess) onSuccess();
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Failed to create pickup request');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (success) {
    return (
      <div className="card text-center bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-xl py-10">
        <CheckCircle2 className="h-16 w-16 text-emerald-400 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-white mb-2">Pickup Request Submitted!</h3>
        <p className="text-gray-300">Your waste collection request has been scheduled.</p>
      </div>
    );
  }

  return (
    <div className="card bg-[#12121a]/85 backdrop-blur-md border border-white/10 shadow-xl">
      <h2 className="text-xl font-bold text-white mb-4">Request Pickup</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-white mb-1.5">
            Waste Category
          </label>
          <select
            value={formData.waste_category}
            onChange={(e) => setFormData({ ...formData, waste_category: e.target.value })}
            className="input-field bg-[#161625] text-white"
            required
          >
            <option value="plastic" className="bg-[#161625] text-white">Plastic</option>
            <option value="cardboard" className="bg-[#161625] text-white">Cardboard</option>
            <option value="paper" className="bg-[#161625] text-white">Paper</option>
            <option value="metal" className="bg-[#161625] text-white">Metal</option>
            <option value="glass" className="bg-[#161625] text-white">Glass</option>
            <option value="compost" className="bg-[#161625] text-white">Compost / Organic</option>
            <option value="e_waste" className="bg-[#161625] text-white">E-Waste</option>
            <option value="trash" className="bg-[#161625] text-white">General Trash</option>
          </select>
        </div>

        <div className="bg-eco-950/40 border border-eco-500/30 rounded-xl p-3 mb-4 text-sm text-eco-300">
          <strong>📍 Pick your location:</strong> Click anywhere on the map below to set the pickup point.
        </div>

        <div className="mb-4 rounded-xl overflow-hidden border border-white/15 shadow-inner" style={{ height: 260 }}>
          <MapContainer center={[formData.latitude, formData.longitude]} zoom={13} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap contributors' />
            <MapPicker position={[formData.latitude, formData.longitude]} setPosition={(p) => setFormData({ ...formData, latitude: p[0], longitude: p[1] })} />
          </MapContainer>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-semibold text-white mb-1.5">
              <MapPinIcon className="inline h-4 w-4 mr-1 text-eco-400" />
              Latitude
            </label>
            <input
              type="number"
              step="0.0001"
              value={formData.latitude}
              readOnly
              className="input-field bg-white/5 border-white/10 text-white font-mono"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-white mb-1.5">
              <MapPinIcon className="inline h-4 w-4 mr-1 text-eco-400" />
              Longitude
            </label>
            <input
              type="number"
              step="0.0001"
              value={formData.longitude}
              readOnly
              className="input-field bg-white/5 border-white/10 text-white font-mono"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-semibold text-white mb-1.5">
              <Calendar className="inline h-4 w-4 mr-1 text-eco-400" />
              Pickup Date
            </label>
            <input
              type="date"
              value={formData.scheduled_date}
              onChange={(e) => setFormData({ ...formData, scheduled_date: e.target.value })}
              className="input-field bg-[#161625] text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-white mb-1.5">
              Time Window
            </label>
            <select
              value={formData.scheduled_window}
              onChange={(e) => setFormData({ ...formData, scheduled_window: e.target.value })}
              className="input-field bg-[#161625] text-white"
            >
              <option value="09:00-11:00" className="bg-[#161625] text-white">09:00 - 11:00</option>
              <option value="11:00-13:00" className="bg-[#161625] text-white">11:00 - 13:00</option>
              <option value="13:00-15:00" className="bg-[#161625] text-white">13:00 - 15:00</option>
              <option value="15:00-17:00" className="bg-[#161625] text-white">15:00 - 17:00</option>
              <option value="17:00-19:00" className="bg-[#161625] text-white">17:00 - 19:00</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-white mb-1.5">
            <Package className="inline h-4 w-4 mr-1 text-eco-400" />
            Load Units (bags/items)
          </label>
          <input
            type="number"
            min="1"
            max="20"
            value={formData.load_units}
            onChange={(e) => setFormData({ ...formData, load_units: parseInt(e.target.value) || 1 })}
            className="input-field bg-[#161625] text-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-white mb-1.5">
            <FileText className="inline h-4 w-4 mr-1 text-eco-400" />
            Description (Optional)
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="input-field bg-[#161625] text-white placeholder-gray-400"
            rows={3}
            placeholder="Additional notes about the waste..."
          />
        </div>

        {error && (
          <div className="p-3 bg-red-950/40 border border-red-500/30 rounded-xl text-sm text-red-200">
            {error}
          </div>
        )}

        <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
          {isSubmitting ? 'Submitting...' : 'Submit Pickup Request'}
        </button>
      </form>
    </div>
  );
};
