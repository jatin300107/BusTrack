from fastapi import FastAPI

app = FastAPI()
from auth import auth
app.include_router(auth)