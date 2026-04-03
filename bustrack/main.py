from fastapi import FastAPI

app = FastAPI()
from bustrack.auth.auth import auth
app.include_router(auth)
from bustrack.admin.admin import admin
app.include_router(admin)