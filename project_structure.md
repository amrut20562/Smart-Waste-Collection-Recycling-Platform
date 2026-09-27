# Project Structure

```text
smart-waste-ai/
│
├── README.md
├── .gitignore
├── docker-compose.yml                 # optional, not required for hackathon
│
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── waste_category.py
│   │   │   ├── waste_scan.py
│   │   │   ├── pickup.py
│   │   │   ├── vehicle.py
│   │   │   └── route.py
│   │   ├── schemas/
│   │   │   ├── vision.py
│   │   │   ├── pickup.py
│   │   │   ├── route.py
│   │   │   └── analytics.py
│   │   ├── api/
│   │   │   ├── health.py
│   │   │   ├── vision.py
│   │   │   ├── pickups.py
│   │   │   └── admin.py
│   │   ├── services/
│   │   │   ├── vision_service.py
│   │   │   ├── clip_service.py
│   │   │   ├── disposal_service.py
│   │   │   ├── pickup_service.py
│   │   │   ├── priority_service.py
│   │   │   ├── clustering_service.py
│   │   │   ├── routing_service.py
│   │   │   └── analytics_service.py
│   │   ├── repositories/
│   │   │   ├── pickup_repository.py
│   │   │   └── route_repository.py
│   │   └── seed.py
│   ├── models/
│   │   └── waste_yolo.pt
│   ├── uploads/
│   └── tests/
│       ├── test_health.py
│       ├── test_vision.py
│       ├── test_priority.py
│       ├── test_clustering.py
│       └── test_routing.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── WasteScanner.tsx
│   │   │   ├── DisposalCard.tsx
│   │   │   ├── PickupForm.tsx
│   │   │   ├── RequestTable.tsx
│   │   │   ├── OperationsMap.tsx
│   │   │   ├── RouteResults.tsx
│   │   │   └── StatCard.tsx
│   │   ├── pages/
│   │   │   ├── CitizenPage.tsx
│   │   │   └── AdminPage.tsx
│   │   ├── hooks/
│   │   ├── types/
│   │   └── styles/
│   └── public/
│
└── docs/
    ├── architecture.md
    ├── tech_stack.md
    ├── hard_constraints.md
    ├── api_contract.md
    ├── database_schema.md
    ├── ai_pipeline.md
    ├── routing.md
    ├── frontend.md
    ├── testing.md
    ├── demo_script.md
    ├── deployment.md
    └── sources.md
```
