from shapely.geometry import LineString, Point
from api_sevices import get_coordinates
from bustrack.model import Route , LocationUpdate , Bus
from sqlmodel import Session , select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api_sevices import get_coordinates , get_distance
from datetime import datetime, time


def distance_from_route(route_coords, passenger_lat, passenger_lon):
    line = LineString(route_coords)  
    point = Point(passenger_lon, passenger_lat)

    return line.distance(point)

def check_passenger_position_on_route(address  , route , db:Session):
    coordinates = get_coordinates(address=address)
    
    distance = distance_from_route(route_coords=route.geometry ,passenger_lat= coordinates[0] , passenger_lon=coordinates[1])
    distance *= 100000
    if distance < 50:
        return None
    elif distance > 50:
        return distance
    

def get_waiting_time(db : Session , location_update, passenger_location):
    
    passenger_coordinates=get_coordinates(address=passenger_location)
    bus = db.get(Bus , location_update.bus_id)
    bus_location = [location_update.longitude , location_update.latitude]
    distance_btw_passenger_n_bus = get_distance(start=bus_location , end=passenger_coordinates)
    time_diff_in_records = datetime.utcnow() - location_update.timestamp
    actual_distance_at_present = distance_btw_passenger_n_bus - (location_update.speed * time_diff_in_records)
    remaining_distance = max(actual_distance_at_present, 0)
    waiting_time = remaining_distance / location_update.speed
    waiting_time_in_mins = waiting_time / 6
    return waiting_time_in_mins





