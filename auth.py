from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from utils import verify_register_details
from create_db import get_session
from model import User, Role

auth = APIRouter()


@auth.get('/')
def home():
    return {"msg": "BusTrack API is running"}


class RegisterUser(SQLModel):
    username: str
    password: str
    email: str
    role: Optional[Role] = Role.user


@auth.post('/register')
def register(user : RegisterUser, db : Session = Depends(get_session)):
    error = verify_register_details(user, db)
    if error is not None:
        return error
    
    # Proceed with registration if no error
    new_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
        role_id=user.role.id if user.role else None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.id}

