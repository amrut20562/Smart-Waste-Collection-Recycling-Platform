# 2-Minute Judge Demo Script

## 0:00 — Problem

"Waste pickup is usually handled as separate requests. The problem is that the collection side still has to decide what matters first and how to group pickups efficiently."

## 0:15 — Citizen AI

Upload a waste image.

Show:

- bounding box
- category
- YOLO score
- disposal instructions

Say:

"The citizen doesn't have to know the waste category manually. The system identifies it and provides deterministic disposal guidance."

## 0:35 — Pickup

Click `Request Pickup`.

Show request created.

## 0:45 — Admin

Switch to admin command center.

Show 15–25 seeded pickup requests on map.

Point out high-priority requests.

## 1:00 — Cluster

Click `Find Clusters`.

Show requests grouped geographically.

Say:

"Instead of treating every pickup independently, we group nearby requests before routing."

## 1:15 — Optimize

Click `Optimize Collection`.

Show:

- vehicles
- stop order
- capacity
- baseline estimated distance
- optimized estimated distance
- calculated reduction percentage

Say:

"OR-Tools then solves a capacity-constrained vehicle-routing problem for these pickup clusters."

## 1:40 — Explainability

Open one route/priority item.

Show why it was prioritized and why a route was selected.

## 1:50 — Close

"The key difference is that this is not only a waste-pickup form. It connects computer vision on the citizen side to optimization on the collection side."
