import openrouteservice
import json
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("API_KEY")) 
API_KEY = os.getenv("API_KEY")
 # debug this
if not API_KEY:
    raise ValueError("Api key not found")
client = openrouteservice.Client(key=API_KEY)

def get_route_properties(start, end, preference="recommended"):
    route = client.directions(
        coordinates=[start, end],
        profile="driving-car",
        format="geojson",
        preference=preference        # <-- add this
    )
    
    feature = route["features"][0]
    distance = feature["properties"]["summary"]["distance"]
    geometry = feature["geometry"]["coordinates"]
    
    return distance, geometry


def get_route_geometry(start,end):


    route = client.directions(
        coordinates=[start , end],
        profile="driving-car",
        format="geojson"
    )
    route_geometry= route["features"][0]["geometry"]["coordinates"]
    return route_geometry
def get_coordinates(address):
    address = client.pelias_search(text=address)["features"][0]["geometry"]["coordinates"]
    return address

def get_address(coordinates):
    result = client.pelias_reverse(coordinates)["features"][0]["geometry"]["label"]
    return result


