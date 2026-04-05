from jose import jwt
from bustrack.config import SECRET_KEY , ALGORITHM
from fastapi import HTTPException , Depends
from bustrack.model import User , Bus
from sqlmodel import Session, select
from create_db import get_session
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
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

def require_admin(token : str= Depends(oauth2_scheme), db : Session = Depends(get_session)):
    user_id = get_user_id_from_token(token)
    user_details = get_user_details(user_id , db)
    if user_details["role"] != "admin":
        return HTTPException(status_code=404 , detail = "Invalid role")
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