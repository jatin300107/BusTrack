from enum import Enum
from typing import Optional , List
from sqlmodel import Relationship, SQLModel, Field

class Role(str, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    user : List["User"] = Relationship(back_populates="role")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    role: Optional[Role] = Relationship(back_populates="user")
    role_id : Optional[int] = Field(default=None,foreign_key="role.id")
