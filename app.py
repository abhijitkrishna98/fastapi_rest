from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from db import SessionLocal,mongo_collection
from schema import UserCreate
from models import User
# import uvicorn
# import logging
app= FastAPI()
# def get_user_data(user):
#     return {
#         "first_name": user.get("full_name").split()[0],
#         "password": user.get("password"),
#         "email": user.get("email"),
#         "phone": user.get("password"),
#     }
@app.post("/register/")
def register_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = User(**user.model_dump(exclude={"profile_picture_path"}))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or Phone already exists")
    finally:
        db.close()

    profile_data = {"user_id": int(db_user.id), "profile_picture_path": user.profile_picture_path}
    mongo_collection.insert_one(profile_data)
    mongo_query= mongo_collection.find_one({"user_id": db_user.id},{'_id': 0})
    return {"user_details":db_user, "profile_picture":mongo_query}

# FastAPI route to get user details by user_id
@app.get("/user/{user_id}/")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    mongo_query= mongo_collection.find_one({"user_id": user_id}, {'_id': 0})
    # with open ("mongo.txt","a+") as f:
    #     f.write(str(mongo_query))
    #     f.write("/n")
    # m_query= 
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # return user
    return {"user_details":user, "profile_picture":str(mongo_query)}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

