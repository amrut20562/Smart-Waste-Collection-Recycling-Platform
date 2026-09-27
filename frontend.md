# Frontend Specification

## Routes/pages

### `/`
Landing/dashboard entry. Provide two clear actions:

- `Citizen`
- `Admin`

### `/citizen`

Sections:

1. Waste Scanner
2. Disposal Guidance
3. Create Pickup
4. My Requests

### `/admin`

Sections:

1. KPI cards
2. Priority requests
3. Interactive map
4. Cluster view
5. Route optimizer
6. Request table
7. Collection statistics

## Citizen scanner

Flow:

```text
Upload / camera input
      ↓
Preview
      ↓
Analyze Waste
      ↓
Detection overlay + category + score/source
      ↓
Disposal instructions
      ↓
Request Pickup
```

Show loading state during inference.

Do not hide the AI source.

Example badge:

`Detected by YOLO · 94% score`

For fallback:

`YOLO uncertain · classified by CLIP fallback`

## Pickup form

Fields:

- waste category
- pickup date
- time window
- location latitude/longitude or selected map point
- load size
- optional description

For the hackathon, allow selecting from demo map points instead of forcing real geocoding.

## Admin dashboard

Top KPI cards:

- Pending
- High Priority
- Active Routes
- Completed Today
- Estimated Distance Saved

Map markers:

- pending requests
- high-priority requests
- cluster centroids
- vehicles

Route action:

`Optimize Collection`

After optimization show a modal/panel with:

- routes
- vehicle loads
- distance comparison
- cluster count

## Visual style

- Modern civic-tech dashboard.
- Clean white/dark neutral UI with green environmental accents.
- Use cards, badges, map, tables, and simple charts.
- Avoid excessive animations.
- Use a single coherent design system.

## Empty/error states

Every major section needs:

- loading state
- empty state
- error state

Never show a blank panel while an API call is failing.
