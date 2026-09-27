export interface VisionDetection {
  category: string;
  confidence: number;
  bbox: number[];
}

export interface DisposalInfo {
  waste_stream: string;
  instructions: string[];
  special_handling: boolean;
  warning: string | null;
}

export interface VisionResult {
  success: boolean;
  category: string;
  display_name: string;
  source: string;
  score: number;
  detections: VisionDetection[];
  disposal: DisposalInfo;
  explanation?: string;
}

export type PickupStatus = 'PENDING' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';

export interface PickupRequest {
  id: number;
  user_id: number;
  waste_category: string;
  description: string | null;
  latitude: number;
  longitude: number;
  scheduled_date: string;
  scheduled_window: string | null;
  load_units: number;
  priority_score: number;
  priority_reasons_json: string | null;
  status: PickupStatus;
  created_at?: string;
  updated_at?: string;
}

export interface PickupCreateRequest {
  user_id: number;
  waste_category: string;
  latitude: number;
  longitude: number;
  scheduled_date: string;
  scheduled_window?: string;
  load_units: number;
  description?: string;
}

export interface Vehicle {
  id: number;
  name: string;
  capacity_units: number;
  active: boolean;
  start_latitude: number;
  start_longitude: number;
}

export interface VehicleRoute {
  vehicle_id: number;
  stops: number[];
  load_units: number;
  capacity_units: number;
  distance_km: number;
}

export interface RouteMetrics {
  baseline_distance_km: number;
  optimized_distance_km: number;
  estimated_reduction_pct: number;
}

export interface RouteOptimizeResponse {
  route_run_id: number;
  solver_status: string;
  vehicles: VehicleRoute[];
  metrics: RouteMetrics;
}

export interface ClusterItem {
  cluster_id: number;
  pickup_request_ids: number[];
  centroid: [number, number];
  request_count: number;
}

export interface AdminOverview {
  total_requests: number;
  pending: number;
  assigned: number;
  completed: number;
  high_priority: number;
  hotspot_count: number;
  active_vehicles: number;
}
