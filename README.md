# FestiMobility

[Version FR](https://github.com/CoopCodeCommun/FestiMobility/blob/main/README_FR.md)

## Overview
FestiMobility is a web application for sustainable mobility management, making carpooling easy for events such as festivals or concerts. It connects drivers proposing rides and passengers seeking to attend an event, with interactive map visualization.

## Main Features
- Two user types: drivers and passengers
- Ride proposals with schedules and departure/arrival points
- Search and filter rides
- Interactive map (OpenStreetMap & Leaflet)
- Smart ride matching (Valhalla)
- Internal messaging system
- Booking and seat management
- Notifications

## Technologies
- Django 5.2
- HTMX
- Bootstrap 5
- OpenStreetMap & Leaflet
- Valhalla (route calculation)
- Mapbox Matrix API (MVP)
- poetry
- PostgreSQL (recommended)
- RESTful API
- TDD (Test Driven Development)

---

## Routing & Matching: Two Approaches

FestiMobility offers two methods for route calculation and driver/passenger matching:

### 1. Mapbox Matrix API (MVP Solution)

- **Principle**: Uses the Mapbox cloud API to calculate distances/durations between points (drivers, passengers).
- **Pros**:
  - Fast integration (REST API, no infrastructure to manage)
  - Maintained map data and algorithms from Mapbox
  - Good support and documentation
- **Cons**:
  - Usage limits depending on plan (paid above free quota)
  - Reliance on a third-party service (GDPR to consider)
  - Less customization possible

**→ This solution is prioritized for the MVP to accelerate development and user testing.**

### 2. Valhalla (Open Source, In Development)

- **Principle**: Self-hosted open source routing server based on OpenStreetMap.
- **Pros**:
  - Data sovereignty
  - Advanced customization (profiles, algorithms, etc.)
  - No recurring costs for external services
- **Cons**:
  - More complex setup and technical maintenance
  - Requires server resources

**→ Valhalla integration remains a target for the stable version, to ensure full control over costs and data.**

---

### Demo Scripts

- `valhalla_matching_example.py`: Matching example using Valhalla (requires local server)
- `demo_mapbox_matrix.py`: Equivalent example using Mapbox API (API key required)

See each script for specific instructions.

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd FestiMobility
   ```
2. Copy the environment example file:
   ```bash
   cp env_example .env
   ```
   Edit variables as needed (database, Django secret, etc.)
3. Install Python dependencies with poetry:
   ```bash
   poetry install
   ```
4. Prepare Valhalla routing data (OSM + tiles):
   ```bash
   make install
   ```
   By default, this command now downloads a minimal OSM extract around Châteauroux (very small area, for testing only), generates Valhalla tiles, and prepares the `./valhalla_data` folder. The Python example has also been adapted to use only coordinates in this area.
5. Start Valhalla (routing API) and PostgreSQL:
   ```bash
   make valhalla-up
   ```
   Services will be available at http://localhost:8002 (Valhalla) and localhost:5432 (PostgreSQL). Variables from .env are automatically loaded by docker-compose.
6. Apply Django migrations:
   ```bash
   poetry run python manage.py migrate
   ```
7. Start the Django server:
   ```bash
   poetry run python manage.py runserver
   ```

### Useful Makefile commands
- `make install` : prepare Valhalla data
- `make valhalla-up` : start Valhalla and PostgreSQL in background
- `make valhalla-down` : stop services
- `make valhalla-clean` : remove all generated data

## Tests
TDD is the preferred approach. To run tests:
```bash
poetry run python manage.py test
```

## Contribution
Please refer to the specifications (`cahier_des_charges.md`) before contributing.

## License
AGPLv3
