import type {
  VisionResult,
  PickupRequest,
  PickupCreateRequest,
  Vehicle,
  RouteOptimizeResponse,
  ClusterItem,
  AdminOverview,
  PickupStatus
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Health
  async health() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  // Vision
  async classifyWaste(imageFile: File): Promise<VisionResult> {
    const formData = new FormData();
    formData.append('image', imageFile);
    const res = await fetch(`${API_BASE}/vision/classify`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error?.message || 'Classification failed');
    }
    return res.json();
  },

  // Pickups
  async createPickup(data: PickupCreateRequest): Promise<PickupRequest> {
    const res = await fetch(`${API_BASE}/pickups`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create pickup request');
    return res.json();
  },

  async getPickups(status?: PickupStatus): Promise<PickupRequest[]> {
    const url = status ? `${API_BASE}/pickups?status=${status}` : `${API_BASE}/pickups`;
    const res = await fetch(url);
    return res.json();
  },

  async getPickup(id: number): Promise<PickupRequest> {
    const res = await fetch(`${API_BASE}/pickups/${id}`);
    return res.json();
  },

  async updatePickupStatus(id: number, status: PickupStatus): Promise<PickupRequest> {
    const res = await fetch(`${API_BASE}/pickups/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    return res.json();
  },

  // Admin
  async getAdminOverview(): Promise<AdminOverview> {
    const res = await fetch(`${API_BASE}/admin/overview`);
    return res.json();
  },

  async getVehicles(): Promise<Vehicle[]> {
    const res = await fetch(`${API_BASE}/admin/vehicles`);
    return res.json();
  },

  async recalculatePriorities() {
    const res = await fetch(`${API_BASE}/admin/prioritize`, { method: 'POST' });
    return res.json();
  },

  async getClusters(): Promise<ClusterItem[]> {
    const res = await fetch(`${API_BASE}/admin/clusters`, { method: 'POST' });
    return res.json();
  },

  async optimizeRoutes(vehicleIds: number[], pickupIds: number[]): Promise<RouteOptimizeResponse> {
    const res = await fetch(`${API_BASE}/admin/routes/optimize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vehicle_ids: vehicleIds,
        pickup_request_ids: pickupIds,
      }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error?.message || 'Route optimization failed');
    }
    return res.json();
  },

  async resetDemo() {
    const res = await fetch(`${API_BASE}/admin/reset-demo`, { method: 'POST' });
    return res.json();
  },
};
