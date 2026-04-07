from shapely.geometry import LineString, Point

def is_on_route(route_coords, passenger_lat, passenger_lon, threshold_meters=50):
    line = LineString(route_coords)  # [[lon, lat], [lon, lat], ...]
    point = Point(passenger_lon, passenger_lat)
    # Shapely distance is in degrees, ~0.00001 deg ≈ 1 meter
    return line.distance(point) < (threshold_meters * 0.00010)