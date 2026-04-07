import openrouteservice
import json
from bustrack.config import api_key
client = openrouteservice.Client(key=api_key)

def get_route_properties(start,end):


    route = client.directions(
        coordinates=[start , end],
        profile="driving-car",
        format="geojson"
    )
    route_summary = route["features"][0]["properties"]["summary"]
    return route_summary

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