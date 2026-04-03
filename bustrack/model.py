from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List


class BusDriverLink(SQLModel, table=True):
    bus_id: Optional[int] = Field(default=None, foreign_key="bus.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")
    buses: List["Bus"] = Relationship(back_populates="drivers", link_model=BusDriverLink)


class Bus(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bus_code: str
    drivers: List["User"] = Relationship(back_populates="buses", link_model=BusDriverLink)
    current_location: str
    avg_speed: int


class RouteStopLink(SQLModel, table=True):
    route_id: Optional[int] = Field(default=None, foreign_key="route.id", primary_key=True)
    stop_id: Optional[int] = Field(default=None, foreign_key="stop.id", primary_key=True)


class Stop(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    order_index: int
    routes: List["Route"] = Relationship(back_populates="stops", link_model=RouteStopLink)


class Route(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_point: str
    end_point: str
    total_distance: float
    stops: List["Stop"] = Relationship(back_populates="routes", link_model=RouteStopLink)


class Schedule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bus_id: Optional[int] = Field(default=None, foreign_key="bus.id")
    driver_id: Optional[int] = Field(default=None, foreign_key="user.id")
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    start_time: str
    end_time: str


class Favourite(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")