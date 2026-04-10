from fastapi import APIRouter , Depends , HTTPException
from create_db import get_session
from sqlmodel import Session , select 
from bustrack.admin.utils import required_role , get_route_list
from bustrack.model import Route , Bus , LocationUpdate
from pydantic import BaseModel
from bustrack.passenger.passenger_service import get_waiting_time , check_passenger_position_on_route
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
def get_bus(bus_id : int , location : Current_location , user = Depends(required_role(role="passenger")) , db : Session = Depends(get_session)):
        location_update = db.exec(select(LocationUpdate).where(LocationUpdate.bus_id==bus_id)).first()
        route = db.exec(select(Route).where(Route.id==location_update.route_id)).first()
        distance = check_passenger_position_on_route(address=location.current_location,route=route , db=db)
        if distance:
                return {"Distance to route" : distance}
        waiting_time = get_waiting_time(db=db , location_update=location_update, passenger_location=location.current_location)
        return {"waiting time" : waiting_time }

