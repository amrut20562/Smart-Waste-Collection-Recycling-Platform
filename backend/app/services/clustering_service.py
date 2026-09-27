import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Dict, Any
from app.config import settings
from app.models.pickup import PickupRequest

class ClusteringService:
    @classmethod
    def cluster_pickups(cls, pickups: List[PickupRequest], eps_meters: int = None, min_samples: int = None) -> List[Dict[str, Any]]:
        if not pickups:
            return []

        if eps_meters is None:
            eps_meters = settings.DBSCAN_EPS_METERS
        if min_samples is None:
            min_samples = settings.DBSCAN_MIN_SAMPLES

        # Earth radius in meters
        EARTH_RADIUS_METERS = 6371000.0
        eps_radians = eps_meters / EARTH_RADIUS_METERS

        coords = np.array([[p.latitude, p.longitude] for p in pickups])
        coords_radians = np.radians(coords)

        # Run DBSCAN with haversine metric
        db = DBSCAN(eps=eps_radians, min_samples=min_samples, metric='haversine')
        labels = db.fit_predict(coords_radians)

        # Group by cluster label
        clusters_dict: Dict[int, List[int]] = {}
        for idx, label in enumerate(labels):
            if label not in clusters_dict:
                clusters_dict[label] = []
            clusters_dict[label].append(idx)

        results: List[Dict[str, Any]] = []

        # Process core clusters (label >= 0)
        cluster_counter = 1
        for label, idx_list in sorted(clusters_dict.items()):
            if label == -1:
                continue # Handle noise separately
            cluster_pickups = [pickups[i] for i in idx_list]
            centroid_lat = float(np.mean([p.latitude for p in cluster_pickups]))
            centroid_lon = float(np.mean([p.longitude for p in cluster_pickups]))
            results.append({
                "cluster_id": cluster_counter,
                "pickup_request_ids": [p.id for p in cluster_pickups],
                "centroid": [round(centroid_lat, 5), round(centroid_lon, 5)],
                "request_count": len(cluster_pickups)
            })
            cluster_counter += 1

        # Process noise points (label == -1) as individual singleton clusters
        if -1 in clusters_dict:
            for i in clusters_dict[-1]:
                p = pickups[i]
                results.append({
                    "cluster_id": cluster_counter,
                    "pickup_request_ids": [p.id],
                    "centroid": [round(p.latitude, 5), round(p.longitude, 5)],
                    "request_count": 1
                })
                cluster_counter += 1

        return results
