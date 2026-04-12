from sqlmodel import SQLModel, Relationship, Field ,  Column , JSON
from typing import Optional, List
from datetime import datetime, time



class RouteStopLink(SQLModel, table=True):
    route_id: Optional[int] = Field(default=None, foreign_key="route.id", primary_key=True)
    stop_id: Optional[int] = Field(default=None, foreign_key="stop.id", primary_key=True)
    order_index: int  # moved here from Stop


# ── Core tables ──────────────────────────────────────────

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")


class Bus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bus_code: str
    avg_speed: float  # int → float, speed isn't always whole


class Stop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    latitude: float
    longitude: float
    routes: List["Route"] = Relationship(back_populates="stops", link_model=RouteStopLink)


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    geometry : Optional[List[List[float]]] = Field(default=None, sa_column=Column(JSON))
    total_distance: float
    stops: List["Stop"] = Relationship(back_populates="routes", link_model=RouteStopLink)


class Schedule(SQLModel, table=True):
    """The single source of truth: who drives which bus on which route, when."""
    id: Optional[int] = Field(default=None, primary_key=True)
    bus_id: Optional[int] = Field(default=None, foreign_key="bus.id")
    driver_id: Optional[int] = Field(default=None, foreign_key="user.id")
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    start_time: datetime
    end_time: datetime


class LocationUpdate(SQLModel, table=True):
    """Append-only tracking log. Never overwrite — always insert."""
    id: Optional[int] = Field(default=None, primary_key=True)
    bus_id: int = Field(foreign_key="bus.id")
    schedule_id: int = Field(foreign_key="schedule.id")
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # dead reckoning fields
    estimated: bool = Field(default=False)  # True = interpolated, not GPS


class Favourite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")