from fastapi import APIRouter , Depends , HTTPException
from create_db import get_session
from sqlmodel import Session , select 
from bustrack.admin.utils import required_role 
from bustrack.model import Schedule ,Bus , Route , LocationUpdate
from pydantic import BaseModel
from bustrack.api_sevices import get_coordinates
driver = APIRouter()

@driver.get('/schedule')
def get_schedule(user = Depends(required_role("driver")) , db : Session = Depends(get_session)):
    schedule = db.exec(select(Schedule).where(Schedule.driver_id==user.id)).first()
    bus = db.get(Bus , schedule.bus_id)
    route = db.get(Route , schedule.route_id)
    return {"Bus code" : bus.bus_code ,
            "Route name" : route.name ,
            "Schedule start timing" : schedule.start_time , 
            "Schedule ending time" : schedule.end_time}
class Bus_info(BaseModel):
    avg_speed : float
    current_location : str
@driver.put('/update-bus-location')
def update_location( info : Bus_info ,user = Depends(required_role("driver")) , db : Session = Depends(get_session)):
    schedule = db.exec(select(Schedule).where(Schedule.driver_id==user.id)).first()
    
    location_update = db.exec(select(LocationUpdate).where(LocationUpdate.schedule_id==schedule.id)).first()
    location_update.speed = info.avg_speed
    coords = get_coordinates(info.current_location)
    location_update.longitude = coords[0]
    location_update.latitude = coords[1]
    db.add(location_update)
    db.commit()

    return {"msg" : "Location updated"} 

    

