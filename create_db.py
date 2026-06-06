from sqlmodel import SQLModel, create_engine, Session

from bustrack.model import User, Role
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=".env")

engine = create_engine(os.getenv("SUPABASE_URL"), echo=True)


def create_db():
    SQLModel.metadata.create_all(engine) 
    role_seeding()


def get_session():
    with Session(engine) as session:
        yield session


def role_seeding():
    with Session(engine) as session:
        # Check if any roles exist
        existing_roles = session.query(Role).first()
        if existing_roles is None:
            # Add default roles
            roles = [
                Role(name="admin"),
                Role(name="driver"),
                Role(name="passenger")
            ]
            session.add_all(roles)
            session.commit()
            print("Default roles seeded: admin, driver, passenger")
        else:
            print("Roles already exist, skipping seeding")

if __name__ == "__main__":
    create_db()
