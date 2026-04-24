from shapely.geometry import LineString, Point
from bustrack.api_sevices import get_coordinates
from bustrack.model import Route , LocationUpdate , Bus
from sqlmodel import Session , select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bustrack.api_sevices import get_coordinates , get_distance
from datetime import datetime, time
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    R = 6371000  # Earth radius in meters
    lon1, lat1 = map(radians, coord1)
    lon2, lat2 = map(radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))



def closest_coordinate(route_coords , coords):
    min_dist = float("inf")
    nearest = None
    for route_coord in route_coords:
        d = haversine(route_coord , coords)
        if d < min_dist:
            min_dist = d
            nearest = route_coord
    return nearest


def get_waiting_time(db: Session, location_update, passenger_location, route):
    passenger_coordinates = get_coordinates(address=passenger_location)
    route_geometry = route.geometry

    bus_location = [location_update.longitude, location_update.latitude]

    nearest_bus_coord = closest_coordinate(route_geometry, bus_location)
    bus_index = route_geometry.index(nearest_bus_coord)

    nearest_passenger_coord = closest_coordinate(route_geometry, passenger_coordinates)
    passenger_index = route_geometry.index(nearest_passenger_coord)

    if bus_index >= passenger_index:
        return None  #
    time_diff_seconds = (datetime.utcnow() - location_update.timestamp).total_seconds()
    distance_covered = (location_update.speed / 3.6) * time_diff_seconds

    current_bus_coord = route_geometry[-1]  # fallback
    d = 0
    for i in range(bus_index, len(route_geometry) - 1):
        d += haversine(route_geometry[i], route_geometry[i + 1])
        if d > distance_covered:
            current_bus_coord = route_geometry[i]
            break
    current_bus_index = route_geometry.index(current_bus_coord)
    if current_bus_index >= passenger_index:
        return None  

    distance_to_travel = get_distance(start=current_bus_coord, end=passenger_coordinates)

    waiting_time_in_mins = (distance_to_travel / 1000 / location_update.speed) * 60
    return waiting_time_in_mins

def distance_from_route(route_coords, passenger_lat, passenger_lon):
    nearest_coord = closest_coordinate(route_coords, [passenger_lon, passenger_lat])
    return haversine([passenger_lon, passenger_lat], nearest_coord)
    