from fastapi import APIRouter , Depends , HTTPException
from create_db import get_session
from sqlmodel import Session , select 
from bustrack.admin.utils import required_role , get_route_list
from bustrack.model import Route , Bus , LocationUpdate , Favourite , RouteStopLink , Schedule
from pydantic import BaseModel

from bustrack.passenger.dead_reckoning import get_waiting_time , distance_from_route
from bustrack.api_sevices import get_coordinates
passenger= APIRouter()

@passenger.get('/dashboard')
def passenger_dashboard(user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user['username']} to the passenger dashboard!"}

@passenger.get('/routes')
def get_routes(user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
        route_list =  get_route_list(db)
        
        return route_list

@passenger.get('/routes/{id}/stop')
def get_stops(route_id , user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
        route = db.get(Route , route_id) 
        if not route:
                raise HTTPException(status_code=404 , detail="Route not found")
        stops = route.stops
        stops_name = [{"name" : stop.name , "id" : stop.id} for stop in stops]
        return {"stops" : stops_name}

@passenger.get('/routes/{route_id}/active-bus')
def get_active_bus(route_id: int, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    schedule = db.exec(select(Schedule).where(Schedule.route_id == route_id)).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="No active bus found for this route")
    bus = db.get(Bus, schedule.bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return {"bus_id": bus.id, "bus_code": bus.bus_code}

class Current_location(BaseModel):
        current_location : str

@passenger.post('/buses/{bus_id}/location')
def get_bus(bus_id: int, location: Current_location, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    
    schedule = db.exec(select(Schedule).where(Schedule.bus_id == bus_id)).first()
    if not schedule:
         raise HTTPException(status_code= 404 , detail="No active schedule found on this bus")
    route = db.exec(select(Route).where(Route.id == schedule.route_id)).first()
    if not route:
         raise HTTPException(status_code=404 , detail="Route not found for this bus")
    location_update = db.exec(select(LocationUpdate).where(LocationUpdate.schedule_id == schedule.id)).first()
    if not location_update:
         raise HTTPException(status_code=404 , detail = "No location update found for this bus")
    passenger_coordinates = get_coordinates(address=location.current_location)
    dist_from_route = distance_from_route(route.geometry, passenger_coordinates[1], passenger_coordinates[0])

    THRESHOLD = 500  
    if dist_from_route > THRESHOLD:
        return {
            "message": f"You are {dist_from_route:.0f}m away from this route. Get within {THRESHOLD}m of the route to track this bus.",
            "distance_from_route": dist_from_route
        }

    waiting_time = get_waiting_time(db=db, route=route, location_update=location_update, passenger_location=location.current_location)

    if waiting_time is None:
        return {"message": "Bus has already passed your stop"}

    return {"waiting_time_minutes": waiting_time}

@passenger.post('/favourites/{route_id}')
def add_favourite(route_id: int, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    route = db.get(Route , route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    existing = db.exec(select(Favourite).where(Favourite.user_id == user["id"], Favourite.route_id == route_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favourites")

    fav = Favourite(user_id=user["id"], route_id=route_id)
    db.add(fav)
    db.commit()
    return {"message": "Added to favourites"}



@passenger.get('/favourites')
def list_favourites(user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    favs = db.exec(select(Favourite).where(Favourite.user_id == user["id"])).all()
    if not favs:
        return {"favourites": []}
    
    routes = [db.get(Route, fav.route_id) for fav in favs]
    fav_list = [{"id": route.id, "name": route.name} for route in routes if route]
    return {"favourites": fav_list}



@passenger.delete('/favourites/{route_id}')
def delete_favourite(route_id: int, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    fav = db.exec(select(Favourite).where(Favourite.user_id == user["id"], Favourite.route_id == route_id)).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")

    db.delete(fav)
    db.commit()
    return {"message": "Removed from favourites"}

@passenger.get('/driver-location/{route_id}')
def get_driver_location(route_id: int , db: Session = Depends(get_session)):
    schedule = db.exec(select(Schedule).where(Schedule.route_id==route_id)).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="No active schedule found for this route")
    bus_id = schedule.bus_id
    location_update = db.exec(select(LocationUpdate).where(LocationUpdate.bus_id == bus_id)).first()
    if not location_update:
         raise HTTPException(status_code = 404, detail = "Location update not found")
    return {"latitude": location_update.latitude, "longitude": location_update.longitude}
    
