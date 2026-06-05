from fastapi import FastAPI

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080" , "https://bus-track-gray.vercel.app"],  # restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from bustrack.auth.auth import auth
app.include_router(auth)
from bustrack.admin.admin import admin
app.include_router(admin)
from bustrack.driver.route import driver
app.include_router(driver)
from bustrack.passenger.passenger_endpoint import passenger
app.include_router(passenger)