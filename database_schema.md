# Database Schema

Use SQLite with SQLAlchemy.

## users

- `id`
- `name`
- `email`
- `role` (`CITIZEN` | `ADMIN`)
- `created_at`

Seed one admin and one citizen account.

## waste_categories

- `id`
- `code`
- `display_name`
- `waste_stream`
- `instructions`
- `special_handling`
- `pickup_supported`
- `warning`

## waste_scans

- `id`
- `user_id` nullable
- `image_path`
- `primary_category`
- `source` (`yolo`, `clip_fallback`, `yolo_low_confidence`)
- `score`
- `detections_json`
- `created_at`

## pickup_requests

- `id`
- `user_id`
- `waste_category`
- `description` nullable
- `latitude`
- `longitude`
- `scheduled_date`
- `scheduled_window` nullable
- `load_units` integer
- `priority_score` float
- `priority_reasons_json`
- `status`
- `created_at`
- `updated_at`

## vehicles

- `id`
- `name`
- `capacity_units`
- `active`
- `start_latitude`
- `start_longitude`

Seed 3 vehicles.

## route_runs

- `id`
- `created_at`
- `solver_status`
- `estimated_total_distance_km`
- `baseline_distance_km`
- `estimated_distance_reduction_pct`
- `vehicle_count`

## route_stops

- `id`
- `route_run_id`
- `vehicle_id`
- `pickup_request_id`
- `stop_order`
- `estimated_arrival_minutes`

## constraints

- Do not store raw user passwords in plain text.
- For a hackathon demo, role-switching or pre-seeded accounts is preferable to implementing a full auth stack.
- Do not store uploaded images permanently unless necessary for the product flow.
