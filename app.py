from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from db import SessionLocal,mongo_collection
from schema import UserCreate
from models import User

app= FastAPI()
@app.post("/register/")
def register_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.session.rollback()
        raise HTTPException(status_code=400, detail="Email or Phone already exists")
    finally:
        db.close()

    profile_data = {"user_id": db_user.id, "profile_picture_path": "dp.jpg"}
    mongo_collection.insert_one(profile_data)

    return db_user

# FastAPI route to get user details by user_id
@app.get("/user/{user_id}/")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

