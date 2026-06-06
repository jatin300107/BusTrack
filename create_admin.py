from sqlmodel import Session , select
from create_db import engine
from bustrack.model import User, Role
from bustrack.auth.utils import create_password_hash, assign_role
from passlib.hash import bcrypt


'''with Session(engine) as db:
    admin = db.exec(select(User).where(User.username == "admin")).first()
    if admin:
        db.delete(admin)
        db.commit()
        print("Admin deleted")

with Session(engine) as db:
    role = assign_role("admin", db)
    user = User(
        username="admin",
        password=create_password_hash("admin301"),
        email="admin@bustrack.com",
        role=role,
        role_id=role.id
    )
    db.add(user)
    db.commit()
    print("Admin created") '''

