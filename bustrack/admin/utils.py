from jose import jwt
from bustrack.config import SECRET_KEY , ALGORITHM
from fastapi import HTTPException
from bustrack.model import User
from sqlmodel import Session, select
def get_user_id_from_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_details(user_id, db : Session):
    user = db.exec(select(User).get(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return {"username" : user.username , "role" : user.role.name}



