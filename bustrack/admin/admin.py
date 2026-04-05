from fastapi import APIRouter, Depends

from .utils import get_user_id_from_token , get_user_details , require_admin
admin = APIRouter()

from sqlmodel import Session
from create_db import get_session

@admin.get('/admin/dashboard')
def admin_dashboard(user = Depends(require_admin) , db : Session = Depends(get_session)):
    
    
        return {"msg" : f"Welcome {user["username"]} to the admin dashboard!"}
    
