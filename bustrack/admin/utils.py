from jose import jwt

from fastapi import HTTPException , Depends
from bustrack.model import User , Bus , Schedule , Route  , Role , Stop ,RouteStopLink
from sqlmodel import Session, select
from create_db import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from math import radians, sin, cos, sqrt, atan2
from dotenv import load_dotenv
import os

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
def get_user_id_from_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=404, detail="User id not found")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_details(user_id, db : Session):
    user = db.exec(select(User).where(User.id==user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return {"username" : user.username , "role" : user.role.name}

bearer_scheme = HTTPBearer()

def require_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_session)):
    token = credentials.credentials
    user_id = get_user_id_from_token(token)
    user_details = get_user_details(user_id , db)
    if user_details["role"] != "admin":
        raise HTTPException(status_code=403 , detail = "Invalid role")
    else: 
        return user_details

def list_of_all_buses(db):
    buses = db.exec(select(Bus)).all()
    return buses


def remove_bus(bus_id , db : Session):
    bus = db.get(Bus , bus_id)
    if not bus:
        raise HTTPException(status_code=404 , detail="Bus not found")
    db.delete(bus)
    db.commit()
    return None

def validate_details(schedule , db : Session):
    driver = db.get(User , schedule.driver_id)
    if not driver:
        raise HTTPException(status_code=404 , detail = "Driver doesnt exist")
    elif driver.role.name != "driver":
        raise HTTPException(status_code=400 , detail = "Not a driver")
    
    bus = db.get(Bus , schedule.bus_id)
    if not bus :
        raise HTTPException(status_code=404 , detail="Invalid Bus id")
    
    route = db.get(Route , schedule.route_id)
    if not route:
        raise HTTPException(status_code=404 , detail="Invalid route id")
    


def save_schedule(schedule , db : Session):
    validate_details(schedule=schedule , db = db)
    
    schedule = Schedule(bus_id = schedule.bus_id , 
                        route_id = schedule.route_id , 
                        driver_id = schedule.driver_id , 
                        start_time = schedule.start_time , 
                        end_time = schedule.end_time )
    db.add(schedule)
    db.commit()

def get_drivers_list(db : Session):
    
    driver_role = db.exec(select(Role).where(Role.name == "driver")).first()
    if not driver_role:
        raise HTTPException(status_code=404, detail="Driver role not found")
    drivers = db.exec(select(User).where(User.role_id == driver_role.id)).all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    return drivers


def get_buses_list(db : Session):
    buses = db.exec(select(Bus)).all()
    if not buses:
            raise HTTPException(status_code=404 , detail= " No buses found")
    return buses

def get_route_list(db : Session):
    routes = db.exec(select(Route)).all()
    if not routes:
            raise HTTPException(status_code=404 , detail= " No Routes found")
    return routes
    

def schedule_options(db : Session):
    return {"drivers" : get_drivers_list(db) ,
            "buses" : get_buses_list(db) ,
            "routes" : get_route_list(db)}

def add_stop_to_route(details, db: Session):
    route = db.get(Route, details.route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    stop = db.get(Stop, details.stop_id)
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    link = RouteStopLink(route_id=details.route_id, stop_id=details.stop_id, order_index=details.order_index)
    db.add(link)
    db.commit()
    return {"msg": "Stop added to route"}



def haversine(coord1, coord2):
    R = 6371000  # meters
    lat1, lon1 = radians(coord1[1]), radians(coord1[0])
    lat2, lon2 = radians(coord2[1]), radians(coord2[0])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def is_stop_on_route(stop_coords, geometry, threshold_meters=100):
    return any(haversine(stop_coords, point) <= threshold_meters for point in geometry)