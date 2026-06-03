from fastapi import APIRouter, Depends , HTTPException
from datetime import datetime
from .utils import  required_role , remove_bus , list_of_all_buses , save_schedule , schedule_options , get_route_list , add_stop_to_route , is_stop_on_route
from bustrack.model import User , Schedule
from pydantic import BaseModel 
from sqlmodel import Session , select 
from typing import Optional, List
from create_db import get_session
from bustrack.api_sevices import get_route_properties, get_coordinates
from bustrack.model import Route , RouteStopLink , Stop , Bus
admin = APIRouter()

@admin.get('/admin/dashboard')
def admin_dashboard(user = Depends(required_role(role="admin")) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user['username']} to the admin dashboard!"}
class Bus_details(BaseModel):
       bus_code : str
       avg_speed : float

@admin.post('/admin/add-bus')
def add_bus(bus_detail : Bus_details , user = Depends(required_role("admin")) ,db : Session = Depends(get_session)):
       bus = Bus(bus_code=bus_detail.bus_code , avg_speed=bus_detail.avg_speed)
       db.add(bus)
       db.commit()
       return {"msg" : "Bus added succesfully"}

@admin.get('/admin/list-of-buses')
def get_list_of_buses(user = Depends(required_role("admin")) ,db : Session = Depends(get_session)):
        bus_list = list_of_all_buses(db)
        return {"bus_list" : bus_list }

@admin.delete('/admin/remove-bus/{bus_id}')
def remove_bus_from_system(bus_id : int , user = Depends(required_role("admin")) , db : Session = Depends(get_session)):
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
def create_schedule(schedule_details : ScheduleDetails , user = Depends(required_role("admin")) ,  db : Session = Depends(get_session)):
        save_schedule(schedule= schedule_details , db = db)
        return {"msg" : "schedule created succesfully "}

@admin.get('/admin/schedule-options')
def get_schedule_options(user = Depends(required_role("admin")) ,  db : Session = Depends(get_session)):
        return schedule_options(db)

@admin.get('/admin/get-routes')
def get_routes(user = Depends(required_role("admin")) ,  db : Session = Depends(get_session)):
        return get_route_list(db)

class AddStop(BaseModel):
    route_id: int
    stop_id: int
    order_index: int

@admin.post('/admin/add-stop-to-route')
def add_stop(details: AddStop, user=Depends(required_role("admin")), db: Session=Depends(get_session)):
    return add_stop_to_route(details=details, db=db)



@admin.get('/admin/registered-users')
def get_registered_user(user=Depends(required_role("admin")),db: Session=Depends(get_session)):
       users = db.exec(select(User)).all() 
       users_list = []
       for u in users:
              users_list.append({"username": u.username, "email": u.email, "role": u.role.name})
        
       return  {"users" : users_list}
class Route_Details(BaseModel):
       name : str
       
       stops : Optional[List]
@admin.post('/admin/add-route')
def add_route(route_details : Route_Details , user=Depends(required_role("admin")),db: Session=Depends(get_session)):
        stops_coords = []
        for stop_name in route_details.stops:
               stop = db.exec(select(Stop).where(Stop.name == stop_name)).first()
               if stop is None:
                      raise HTTPException(status_code=404, detail=f"Stop '{stop_name}' not found")
               stops_coords.append([stop.longitude, stop.latitude])
               
        distance , geometry = get_route_properties(stops_coords)
        route = Route(name = route_details.name , total_distance = distance , geometry = geometry)
        db.add(route)
        db.commit()
        db.refresh(route)
        route_stop_list = []
        for i , stop_name in enumerate(route_details.stops):
               stop = db.exec(select(Stop).where(Stop.name == stop_name)).first()
               if not stop:
                      raise HTTPException(status_code=404, detail=f"Invalid stop name: {stop_name}")
    
               stop_coords = [stop.longitude, stop.latitude]  # [lon, lat]
               
               if not is_stop_on_route(stop_coords, geometry):
                        raise HTTPException(status_code=400, detail=f"Stop '{stop_name}' is not on this route")

               route_stop = RouteStopLink(route_id = route.id , stop_id = stop.id, order_index = i)
               route_stop_list.append(route_stop)
        db.add_all(route_stop_list)
        db.commit()
        return {"msg"  : "Route created successfully"}
class Stop_Details(BaseModel) :
       name :str
       address : str

        
@admin.post('/admin/create-stop')
def create_stop(stop_details : Stop_Details , user = Depends(required_role("admin")), db : Session = Depends(get_session)):
        stop_coordinates = get_coordinates(address=stop_details.address)
        if  not stop_coordinates:
               raise HTTPException(status_code=404 , detail= "stop cordinates not found")
        stop = Stop(name=stop_details.name , latitude= stop_coordinates[1] , longitude=stop_coordinates[0])
        db.add(stop)
        db.commit()
        return {"msg" : "Stop created successfully"}

@admin.delete('/admin/{route_id}/delete-route')
def delete_route(route_id :int , user = Depends(required_role("admin")) , db : Session = Depends(get_session)):
       route = db.get(Route , route_id)
       db.delete(route)
       db.commit()
       return {"msg" : "route deleted route successfully"}

@admin.get('/admin/get-all-stops')
def get_all_stops(user = Depends(required_role("admin")) , db : Session = Depends(get_session)):
       stops = db.exec(select(Stop)).all()
       return {"stops" : stops}

@admin.delete('/admin/{schedule_id}/delete-schedule')
def delete_schedule(schedule_id : int , user = Depends(required_role("admin")) , db : Session = Depends(get_session)):
       schedule = db.get(Schedule , schedule_id)
       db.delete(schedule)
       db.commit()
       return {"msg" : "Schedule deleted successfully"}

@admin.get('/admin/get-all-schedules')
def get_all_schedules(user = Depends(required_role("admin")) , db : Session = Depends(get_session)):
       schedules = db.exec(select(Schedule)).all()
       return {"schedules" : schedules}