from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from .utils import get_user_id_from_token , get_user_details
admin = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@admin.get('/admin/dashboard')
def admin_dashboard(token : str= Depends(oauth2_scheme)):
    user_id = get_user_id_from_token(token)
    user_details = get_user_details(user_id)
    if user_details["role"] != "admin":
        return {"msg" : "Access denied. Invalid role"}
    else:
        return {"msg" : f"Welcome {user_details["username"]} to the admin dashboard!"}
    
