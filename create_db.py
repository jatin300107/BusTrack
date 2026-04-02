from sqlmodel import SQLModel, create_engine, Session

from model import User

engine = create_engine("sqlite:///bust_track.db", echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
