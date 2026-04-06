import openrouteservice
import json
client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImJjMzBmMzkxMTM4MTRiODI5NzY0Zjc0NTA3YmRlNjZkIiwiaCI6Im11cm11cjY0In0=")

coords = [[77.2090, 28.6139], [77.2310, 28.6280]]  # [lng, lat]

route = client.directions(
    coordinates=coords,
    profile="driving-car",
    format="geojson"
)

print(json.dumps(route, indent=2))