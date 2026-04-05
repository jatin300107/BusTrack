from fastapi import APIRouter, Depends

from .utils import  require_admin , remove_bus , list_of_all_buses
admin = APIRouter()

from sqlmodel import Session
from create_db import get_session

@admin.get('/admin/dashboard')
def admin_dashboard(user = Depends(require_admin) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user["username"]} to the admin dashboard!"}

@admin.get('/admin/list-of-buses')
def get_list_of_buses(user = Depends(require_admin) ,db : Session = Depends(get_session)):
        bus_list = list_of_all_buses(db)
        return bus_list

@admin.delete('/admin/remove-bus/{bus-id}')
def remove_bus_from_system(bus_id : int , user = Depends(require_admin) , db : Session = Depends(get_session)):
        error = remove_bus(bus_id , db)
        if error:
                return error
        return {"msg" : " Bus removed from system successfully"}

@admin.post()




        
        
    
