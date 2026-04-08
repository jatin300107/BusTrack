from fastapi import APIRouter, Depends , HTTPException
from datetime import datetime
from .utils import  require_admin , remove_bus , list_of_all_buses , save_schedule , schedule_options , get_route_list , add_stop_to_route , is_stop_on_route
from bustrack.model import User
from pydantic import BaseModel 
from sqlmodel import Session , select 
from typing import Optional, List
from create_db import get_session
from api_sevices import get_route_properties, get_coordinates
from bustrack.model import Route , RouteStopLink , Stop
admin = APIRouter()

@admin.get('/admin/dashboard')
def admin_dashboard(user = Depends(require_admin) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user['username']} to the admin dashboard!"}

@admin.get('/admin/list-of-buses')
def get_list_of_buses(user = Depends(require_admin) ,db : Session = Depends(get_session)):
        bus_list = list_of_all_buses(db)
        return {"bus_list" : bus_list }

@admin.delete('/admin/remove-bus/{bus-id}')
def remove_bus_from_system(bus_id : int , user = Depends(require_admin) , db : Session = Depends(get_session)):
        error = remove_bus(bus_id , db)
        if error:
                return error
        return {"msg" : " Bus removed from system successfully"}

class ScheduleDetails(BaseModel):
        bus_id : int
        driver_id : int
        route_id : int
        start_time : datetime
        end_time : datetime

@admin.post('/admin/create-schedule')
def create_schedule(schedule_details : ScheduleDetails , user = Depends(require_admin) ,  db : Session = Depends(get_session)):
        save_schedule(schedule= schedule_details , db = db)
        return {"msg" : "schedule created succesfully "}

@admin.get('/admin/schedule-options')
def get_schedule_options(user = Depends(require_admin) ,  db : Session = Depends(get_session)):
        return schedule_options(db)

@admin.get('/admin/get-routes')
def get_routes(user = Depends(require_admin) ,  db : Session = Depends(get_session)):
        return {"roues" : get_route_list(db)}

class AddStop(BaseModel):
    route_id: int
    stop_id: int
    order_index: int

@admin.post('/admin/add-stop')
def add_stop(details: AddStop, user=Depends(require_admin), db: Session=Depends(get_session)):
    return add_stop_to_route(details=details, db=db)



@admin.get('/admin/registered-users')
def get_registered_user(user=Depends(require_admin),db: Session=Depends(get_session)):
       users = db.exec(select(User)).all() 
       users_list = []
       for user in users:
              users_list.append({user.username : user.role.name})
        
       return  {"List of users" : users_list}
class Route_Details(BaseModel):
       name : str
       start_point : str
       end_point : str
       stops : Optional[List]
@admin.post('/admin/add-route')
def add_route(route_details : Route_Details , user=Depends(require_admin),db: Session=Depends(get_session)):
        start_coordinates = get_coordinates(address=route_details.start_point)
        end_coordinates = get_coordinates(address=route_details.end_point)
        distance , geometry = get_route_properties( start=start_coordinates  , end= end_coordinates)
        route = Route(name = route_details.name , total_distance = distance , geometry = geometry)
        db.add(route)
        db.commit()
        db.refresh(route)
        route_stop_list = []
        for stop_name in route_details.stops:
               stop = db.exec(select(Stop).where(Stop.name == stop_name)).first()
               if not stop:
                      raise HTTPException(status_code=404, detail=f"Invalid stop name: {stop_name}")
    
               stop_coords = [stop.longitude, stop.latitude]  # [lon, lat]
               if not is_stop_on_route(stop_coords, geometry):
                        raise HTTPException(status_code=400, detail=f"Stop '{stop_name}' is not on this route")

               route_stop = RouteStopLink(route_id = route.id , stop_id = stop.id)
               route_stop_list.append(route_stop)
        db.add_all(route_stop_list)
        db.commit()
        return {"msg"  : "Route created successfully"}
        
        
    
