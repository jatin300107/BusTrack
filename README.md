# BusTrack 🚌

A real-time public transport tracking backend for small cities, built with FastAPI.

BusTrack solves the core problem of public transport in smaller Indian cities — passengers have no idea where their bus is or when it will arrive. By combining real Indian transit data with a dead reckoning estimation engine, BusTrack provides live bus location estimates and ETAs without requiring GPS hardware on every vehicle.

---
# Live Link
[Bustrack](https://bus-track-gray.vercel.app/)
---

## How It Works

Drivers periodically update their current location and average speed through the driver portal. When a driver hasn't updated recently, the system automatically estimates the bus's current position using dead reckoning — calculating how far the bus has likely traveled based on its last known position, reported speed, and time elapsed. Passengers query this estimated position to get near real-time estimated location and ETA to their stop.

---

## Features

- **Role-based access** — Passenger, Driver, and Admin roles with JWT authentication
- **Dead reckoning engine** — The system estimates the bus position by projecting its last known coordinates forward using reported speed  and elapsed time.
- **ETA calculation** — ETA is calculated by combining the estimated current bus position with route stop distance using OpenRouteServices
- **Route and stop management** — Admin can manage bus routes, stops, and assign drivers
- **Travel time calculation** — Uses OpenRouteService API for distance and travel time between coordinates
- **Auto-generated API docs** — Interactive documentation at `/docs` via FastAPI Swagger UI

---

## External APIs

| API | Purpose |
|-----|---------|

| [OpenRouteService](https://openrouteservice.org) | Distance and travel time calculation between coordinates (free, no credit card) |

---

## Tech Stack

- **FastAPI** — Backend framework
- **SQLModel** — ORM
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
# Testing Manual : 
[BustrackTestingManual](https://docs.google.com/document/d/12hZiiZV0edQeXOjvxaGS36Ya7Rp0vO8A/edit?usp=drive_link&ouid=112278392948970091818&rtpof=true&sd=true)

---

## Note

This project was inspired by the Smart Cities / Public Transport problem statement from Smart India Hackathon. Backend written independently. Dead reckoning position estimation approach designed as a hardware-free alternative to GPS tracking.
