from shapely.geometry import LineString, Point
from api_sevices import get_coordinates
from bustrack.model import Route
from sqlmodel import Session , select
def distance_from_route(route_coords, passenger_lat, passenger_lon):
    line = LineString(route_coords)  
    point = Point(passenger_lon, passenger_lat)

    return line.distance(point)

def check_passenger_position_on_route(address  , route , db:Session):
    coordinates = get_coordinates(address=address)
    route = db.exec(select(Route).where(Route.name==route)).first()
    distance = distance_from_route(route_coords=route.geometry ,passenger_lat= coordinates[0] , passenger_lon=coordinates[1])
    distance *= 100000
    if distance < 50:
        return None
    elif distance > 50:
        return distance
    



