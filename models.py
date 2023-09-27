from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

from db import engine

Base = declarative_base()
# SQLAlchemy User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    profile_picture_path = Column(String)
