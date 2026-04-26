import openrouteservice
import json
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
import requests


load_dotenv()

 
API_KEY = os.getenv("API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

if not API_KEY:
    raise ValueError("Api key not found")
client = openrouteservice.Client(key=API_KEY)

def get_route_properties(start, end, preference="recommended"):
    route = client.directions(
        coordinates=[start, end],
        profile="driving-car",
        format="geojson",
        preference=preference
    )
    
    feature = route["features"][0]
    distance = feature["properties"]["summary"]["distance"]
    geometry = feature["geometry"]["coordinates"]
    
    return distance, geometry

def get_distance(start, end, preference="recommended"):
    route = client.directions(
        coordinates=[start, end],
        profile="driving-car",
        format="geojson",
        preference=preference
    )
    
    feature = route["features"][0]
    distance = feature["properties"]["summary"]["distance"]
    geometry = feature["geometry"]["coordinates"]
    
    return distance
def get_route_geometry(start,end , preference="recommended"):


    route = client.directions(
        coordinates=[start , end],
        profile="driving-car",
        format="geojson" ,
        preference="recommended"
    )
    route_geometry= route["features"][0]["geometry"]["coordinates"]
    return route_geometry
from geopy.geocoders import Nominatim

def get_coordinates(address):
    res = requests.get(
    "https://api.geoapify.com/v1/geocode/search",
    params={"text": address, "apiKey": os.getenv("GEOAPIFY_API_KEY"), "lang": "en"}
    ).json()
    coords = res["features"][0]["geometry"]["coordinates"]  # already [lng, lat]
    return coords

def get_address(coordinates):
    result = client.pelias_reverse(coordinates)["features"][0]["geometry"]["label"]
    return result


