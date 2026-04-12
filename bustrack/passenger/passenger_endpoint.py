from fastapi import APIRouter , Depends , HTTPException
from create_db import get_session
from sqlmodel import Session , select 
from bustrack.admin.utils import required_role , get_route_list
from bustrack.model import Route , Bus , LocationUpdate , Favourite
from pydantic import BaseModel

from bustrack.passenger.dead_reckoning import get_waiting_time , distance_from_route
from bustrack.api_sevices import get_coordinates
passenger= APIRouter()

@passenger.get('/dashboard')
def passenger_dashboard(user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user['username']} to the passenger dashboard!"}

@passenger.get('/routes')
def get_routes(user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
        return get_route_list(db)

@passenger.get('/routes/{id}/stop')
def get_stops(route_id , user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
        route = db.get(Route , route_id)
        if not route:
                raise HTTPException(status_code=404 , detail="Route not found")
        stops = route.stops.name
        return {"stops" : stops}

class Current_location(BaseModel):
        current_location : str

@passenger.post('/buses/{bus-id}/location')
def get_bus(bus_id: int, location: Current_location, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    
    location_update = db.exec(select(LocationUpdate).where(LocationUpdate.bus_id == bus_id)).first()
    route = db.exec(select(Route).where(Route.id == location_update.route_id)).first()

    
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
    route = db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    existing = db.exec(select(Favourite).where(Favourite.user_id == user.id, Favourite.route_id == route_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favourites")

    fav = Favourite(user_id=user.id, route_id=route_id)
    db.add(fav)
    db.commit()
    return {"message": "Added to favourites"}



@passenger.get('/favourites')
def list_favourites(user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    favs = db.exec(select(Favourite).where(Favourite.user_id == user.id)).all()
    if not favs:
        return {"message": "No favourites yet"}
    
    routes = [db.get(Route, fav.route_id) for fav in favs]
    return {"favourites": routes}



@passenger.delete('/favourites/{route_id}')
def delete_favourite(route_id: int, user=Depends(required_role(role="passenger")), db: Session = Depends(get_session)):
    fav = db.exec(select(Favourite).where(Favourite.user_id == user.id, Favourite.route_id == route_id)).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")

    db.delete(fav)
    db.commit()
    return {"message": "Removed from favourites"}