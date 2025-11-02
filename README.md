## 📦 Project Overview

REST API for managing organizations, their activities, phone numbers, and related buildings. The service relies on PostgreSQL and Redis and comes with dockerised infrastructure plus a data-filler utility to seed demo content.

---

## 🚀 Quick Start

1. **Clone the repo** and move into the project directory.
2. **Copy configuration templates** and adjust values for your environment:
   ```bash
   cp .env.example .env
   cp postgres.env.example postgres.env
   ```
   Required variables:
   - `.env`
     - `API_TOKEN` — token required by the API key middleware.
     - `LOGGING_LEVEL` — application log level (e.g. `INFO`, `DEBUG`).
     - `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME` — database connection settings used by the app.
     - `REDIS_DSN` — Redis connection string (default `redis://redis:6379` for docker-compose).
   - `postgres.env`
     - `POSTGRES_USER`
     - `POSTGRES_PASSWORD`
3. **Start the stack**:
   ```bash
    docker compose up --build -d
   ```
4. **(Optional) Seed demo data** once the containers are up:
   ```bash
   curl -X POST \
     -H "X-API-Key: <API_TOKEN value>" \
     http://localhost:8001/api/v1/filler/fill
   ```
5. API docs are exposed at `http://localhost:8001/api/docs` (remember the API key header).

---

## 🔑 Auth

All requests must include the API key header:

```
X-API-Key: <API_TOKEN>
```

---

## ⚡ Caching

List/detail GET endpoints for organizations, buildings, activities, and phone numbers are cached for ~10 seconds via Redis (powered by `fastapi-cache`). Repeated reads with the same parameters within that window hit the cache.

---

## 🌐 Base URL

```
http://localhost:8001/api/v1
```

---

## 🏢 Organizations API

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET`  | `/organizations` | List organizations (supports rich filtering). |
| `GET`  | `/organizations/{organization_id}` | Get details of a single organization. |
| `POST` | `/organizations` | Create an organization. |
| `PUT`  | `/organizations/{organization_id}` | Update organization attributes. |
| `DELETE` | `/organizations/{organization_id}` | Delete an organization. |
| `POST` | `/organizations/activity` | Assign an activity to an organization. |
| `DELETE` | `/organizations/activity` | Unassign an activity. |
| `POST` | `/organizations/phone-number` | Assign a phone number. |
| `DELETE` | `/organizations/phone-number` | Unassign a phone number. |

### `GET /organizations` query parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | int (default 20) | Max items per page. | `limit=50` |
| `offset` | int (default 0) | Offset for pagination. | `offset=20` |
| `name` | string | Case-insensitive substring match by organization name. | `name=horns` |
| `building_id` | UUID | Filter by building (mutually exclusive with `geo_*`). | `building_id=8db1c5f4-...` |
| `activity_id` | UUID | Filter by activity; includes descendants up to `activities_depth`. | `activity_id=1dcd2a8d-...` |
| `geo_kind` | enum (`radius` \\| `bbox`) | Enables geographic filtering (toggles required parameters below). | `geo_kind=radius` |
| `lat`, `lon`, `radius_m` | float, float, int | Required when `geo_kind=radius`. Filters organizations whose buildings fall within the radius (meters) of the given point. | `lat=55.7558&lon=37.6176&radius_m=5000` |
| `lat_min`, `lat_max`, `lon_min`, `lon_max` | float | Required when `geo_kind=bbox`. Bounding box where latitude/longitude min < max. | `lat_min=55.74&lat_max=55.77&lon_min=37.60&lon_max=37.64` |

> 💡 **Rules**:
> - `building_id` cannot be combined with any `geo_*` parameters.
> - When using `radius`, all of `lat`, `lon`, and `radius_m` must be present.
> - When using `bbox`, all four bounds are required.
> - `activity_id` automatically pulls in child activities up to the depth specified in `activities_depth` (see `.env`).

### Sample queries

- **List first page without filters**  
  `GET /organizations?limit=20&offset=0`

- **Search by name**  
  `GET /organizations?name=market`

- **Filter by building**  
  `GET /organizations?building_id=8c6ba9b7-a7b9-4e83-9d37-0a8f3e30d5f1`

- **Filter by activity tree**  
  `GET /organizations?activity_id=9f542452-5122-46ff-9664-6f2f0d7506a0`

- **Radius search around the seeded building (Moscow center, 3 km)**  
  `GET /organizations?geo_kind=radius&lat=55.7558&lon=37.6176&radius_m=3000`

- **Bounding box example (~1 km span)**  
  `GET /organizations?geo_kind=bbox&lat_min=55.7500&lat_max=55.7600&lon_min=37.6100&lon_max=37.6300`

---

## 🏗 Buildings API

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/buildings` | List buildings (supports pagination). |
| `GET` | `/buildings/{building_id}` | Retrieve a building. |
| `POST` | `/buildings` | Create a building. |
| `PUT` | `/buildings/{building_id}` | Update latitude/longitude/address. |
| `DELETE` | `/buildings/{building_id}` | Remove a building. |

Payloads align with `BuildingIn` / `BuildingUpdate` schemas (`address`, `latitude`, `longitude` — validated ranges).

---

## 🎯 Activities API

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/activities` | List activities with nested children (limited by `activities_depth`). |
| `GET` | `/activities/{activity_id}` | Retrieve one activity with descendants. |
| `POST` | `/activities` | Create a new activity (`name`, optional `parent_id`). |
| `PUT` | `/activities/{activity_id}` | Update activity name/parent. |
| `DELETE` | `/activities/{activity_id}` | Delete an activity. |

---

## ☎️ Phone Numbers API

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/phone-numbers` | List phone numbers. |
| `GET` | `/phone-numbers/{phone_id}` | Fetch a single phone number. |
| `POST` | `/phone-numbers` | Create a phone number. |
| `PUT` | `/phone-numbers/{phone_id}` | Update a phone number string. |
| `DELETE` | `/phone-numbers/{phone_id}` | Delete a phone number. |

---

## 🛠 Utilities

- **Database filler** (`POST /filler/fill`) — populates demo activities, phone numbers, building, and the “Horns and Hooves” organization located at `lat=55.7558`, `lon=37.6176` (Moscow centre). Useful to test geo queries right away.

---

## 🧪 Testing ideas

- After starting the stack and seeding data, try radius/bbox queries as described above.
- Create additional buildings/organizations via REST to validate filtering combinations.

Enjoy exploring! 🧭
