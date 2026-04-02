from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt 
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlmodel import Session, select
from model import Role, User
from datetime import datetime , timedelta
def verify_register_details(user,db : Session):
    existing = db.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400,details="User already exists with this email")
    existing = db.exec(select(User).where(User.username==user.username)).first()
    if existing:
        raise HTTPException(status_code=400,details="Username not available")
    return None

def create_password_hash(password : str):
    return bcrypt.hash(password)

def assign_role(role , db : Session):
    role = db.exec(select(Role).where(Role.name == role)).first()
    if role is None:
        raise HTTPException(status_code=400,details="Invalid role")
    return role
    
def verify_password(plain_password,hashed_password):
    return bcrypt.verify(plain_password,hashed_password)

def verify_login_details(user, db : Session):
    existing = db.exec(select(User).where(User.username==user.username)).first()
    if not existing:
        raise HTTPException(status_code=400,details="Invalid username or password")
    if not verify_password(user.password, existing.password):
        raise HTTPException(status_code=400,details="Invalid username or password")
    return existing

def create_jwt_token(user : User):
    to_encode = {"user_id" : user.id , "username" : user.username , "role" : user.role.name}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)