from app.models.pickup import PickupRequest
from app.services.clustering_service import ClusteringService

def test_dbscan_clustering():
    # Create 3 points close together (Cluster 1) and 1 isolated point
    p1 = PickupRequest(id=1, latitude=18.5360, longitude=73.8950)
    p2 = PickupRequest(id=2, latitude=18.5362, longitude=73.8952)
    p3 = PickupRequest(id=3, latitude=18.5365, longitude=73.8948)
    p_isolated = PickupRequest(id=4, latitude=18.4500, longitude=73.7500)

    pickups = [p1, p2, p3, p_isolated]
    clusters = ClusteringService.cluster_pickups(pickups, eps_meters=750, min_samples=2)

    assert len(clusters) >= 2
    # Cluster with 3 points
    dense_clusters = [c for c in clusters if c["request_count"] == 3]
    assert len(dense_clusters) == 1
    assert 1 in dense_clusters[0]["pickup_request_ids"]
    assert 2 in dense_clusters[0]["pickup_request_ids"]
    assert 3 in dense_clusters[0]["pickup_request_ids"]
