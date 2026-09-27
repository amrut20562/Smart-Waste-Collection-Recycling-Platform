import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { PickupRequest, ClusterItem, Vehicle } from '../types';

// Fix for default marker icons in Leaflet with Webpack/Vite
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

interface OperationsMapProps {
  requests: PickupRequest[];
  clusters?: ClusterItem[];
  vehicles?: Vehicle[];
  center?: [number, number];
  zoom?: number;
}

export const OperationsMap: React.FC<OperationsMapProps> = ({
  requests,
  clusters = [],
  vehicles = [],
  center = [18.5204, 73.8567],
  zoom = 12,
}) => {
  const getMarkerColor = (priority: number) => {
    if (priority >= 70) return '#ef4444'; // red
    if (priority >= 40) return '#f59e0b'; // yellow
    return '#22c55e'; // green
  };

  const createCustomIcon = (color: string) => {
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });
  };

  const vehicleIcon = L.divIcon({
    className: 'vehicle-marker',
    html: `<div style="background-color: #3b82f6; width: 30px; height: 30px; border-radius: 4px; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">🚛</div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });

  return (
    <div className="card p-0 overflow-hidden">
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '500px', width: '100%' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Render pickup request markers */}
        {requests.map((req) => (
          <Marker
            key={req.id}
            position={[req.latitude, req.longitude]}
            icon={createCustomIcon(getMarkerColor(req.priority_score))}
          >
            <Popup>
              <div className="text-sm">
                <div className="font-bold mb-1">Pickup #{req.id}</div>
                <div className="text-gray-600 capitalize">{req.waste_category.replace('_', ' ')}</div>
                <div className="text-gray-600">Load: {req.load_units} units</div>
                <div className="text-gray-600">Priority: {req.priority_score.toFixed(1)}</div>
                <div className="text-gray-600">{req.scheduled_date}</div>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render cluster circles */}
        {clusters.map((cluster) => (
          <Circle
            key={cluster.cluster_id}
            center={[cluster.centroid[0], cluster.centroid[1]]}
            radius={500}
            pathOptions={{
              color: '#22c55e',
              fillColor: '#22c55e',
              fillOpacity: 0.15,
              weight: 2,
            }}
          >
            <Popup>
              <div className="text-sm">
                <div className="font-bold mb-1">Cluster #{cluster.cluster_id}</div>
                <div className="text-gray-600">{cluster.request_count} pickup requests</div>
              </div>
            </Popup>
          </Circle>
        ))}

        {/* Render vehicle depot markers */}
        {vehicles.map((vehicle) => (
          <Marker
            key={vehicle.id}
            position={[vehicle.start_latitude, vehicle.start_longitude]}
            icon={vehicleIcon}
          >
            <Popup>
              <div className="text-sm">
                <div className="font-bold mb-1">{vehicle.name}</div>
                <div className="text-gray-600">Capacity: {vehicle.capacity_units} units</div>
                <div className="text-gray-600">Status: {vehicle.active ? 'Active' : 'Inactive'}</div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};
