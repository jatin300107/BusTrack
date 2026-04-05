from typing import Optional
from pydantic import  BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from bustrack.utils import verify_register_details , create_password_hash , assign_role , verify_login_details , verify_password , create_jwt_token
from create_db import get_session
from bustrack.model import User, Role
from fastapi.security import OAuth2PasswordRequestForm

auth = APIRouter()


@auth.get('/')
def home():
    return {"msg": "BusTrack API is running"}


class RegisterUser(BaseModel):
    username: str
    password: str
    email: str
    role: str


@auth.post('/register')
def register(user : RegisterUser, db : Session = Depends(get_session)):
    error = verify_register_details(user, db)
    if error is not None:
        return error
    hashed_password = create_password_hash(user.password)
    assigned_role = assign_role(user.role,db)
    new_user = User(username = user.username , password = hashed_password , email=user.email , role = assigned_role , role_id=assigned_role.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.id}
class LoginUser(BaseModel):
    username : str
    password : str

@auth.post('/login')
def login(user : LoginUser , db : Session = Depends(get_session)):
    user_obj = verify_login_details(username = user.username, password=user.password ,db =  db)
    token = create_jwt_token(user_obj)
    return {"msg": "Login successful", "access_token": token}
