# BusTrack 🚌

A real-time public transport tracking backend for small cities, built with FastAPI.

BusTrack solves the core problem of public transport in smaller Indian cities — passengers have no idea where their bus is or when it will arrive. By combining real Indian transit data with a dead reckoning estimation engine, BusTrack provides live bus location estimates and ETAs without requiring GPS hardware on every vehicle.

---

## How It Works

Drivers periodically update their current location and average speed through the driver portal. When a driver hasn't updated recently, the system automatically estimates the bus's current position using dead reckoning — calculating how far the bus has likely traveled based on its last known position, reported speed, and time elapsed. Passengers query this estimated position to get real-time location and ETA to their stop.

---

## Features

- **Role-based access** — Passenger, Driver, and Admin roles with JWT authentication
- **Dead reckoning engine** — Estimates bus position between driver updates using speed × time
- **ETA calculation** — Returns estimated arrival time to any stop on the route
- **Route and stop management** — Admin can manage bus routes, stops, and assign drivers
- **Real Indian transit data** — Bus route and stop data sourced from data.gov.in open transit datasets
- **Travel time calculation** — Uses OpenRouteService API for distance and travel time between coordinates
- **Auto-generated API docs** — Interactive documentation at `/docs` via FastAPI Swagger UI

---

## External APIs

| API | Purpose |
|-----|---------|
| [data.gov.in](https://data.gov.in) | Indian government open transit data — bus routes and stops |
| [OpenRouteService](https://openrouteservice.org) | Distance and travel time calculation between coordinates (free, no credit card) |

---

## Tech Stack

- **FastAPI** — Backend framework
- **SQLAlchemy** — ORM
- **SQLite** (dev) / **PostgreSQL** (production)
- **JWT** — Authentication
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

---

## Roles

| Role | Access |
|------|--------|
| Passenger | Query bus location, get ETA to stop |
| Driver | Update current location and speed |
| Admin | Manage routes, stops, buses, assign drivers |

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/buses/{bus_id}/location` | Get estimated current location of a bus |
| GET | `/buses/{bus_id}/eta` | Get ETA to a specific stop |
| POST | `/driver/location` | Driver updates current location and speed |
| GET | `/routes` | List all routes |
| GET | `/routes/{route_id}/stops` | Get all stops on a route |
| POST | `/admin/routes` | Create a new route (admin) |
| POST | `/admin/buses` | Add a new bus (admin) |

---

## Project Status

Backend in development. Frontend planned as a separate phase.

---

## Note

This project was inspired by the Smart Cities / Public Transport problem statement from Smart India Hackathon. Backend written independently. Dead reckoning position estimation approach designed as a hardware-free alternative to GPS tracking.
