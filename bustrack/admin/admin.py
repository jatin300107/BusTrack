from fastapi import APIRouter, Depends
from datetime import datetime
from .utils import  require_admin , remove_bus , list_of_all_buses , save_schedule , schedule_options , get_route_list , add_stop_to_route

from pydantic import BaseModel
from sqlmodel import Session
from create_db import get_session

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



        
        
    
