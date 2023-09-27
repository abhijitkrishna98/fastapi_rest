import io
from PIL import Image
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from db import SessionLocal,mongo_collection
from schema import UserCreate
from models import User

app= FastAPI()
# FastAPI route to register user
@app.post("/register/", status_code=201)
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
    im = Image.open(user.profile_picture_path)
    image_bytes = io.BytesIO()
    im.save(image_bytes, format='JPEG')
    image = {
    'data': image_bytes.getvalue()
    }
    mongo_collection.insert_one(image).inserted_id 
    # mongo_query= mongo_collection.find_one({"user_id": db_user.id},{'_id': 0})
    return {"user_details":db_user,"message":"User Registered!"}

# FastAPI route to get user details by user_id
@app.get("/user/{user_id}/", status_code=200)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    # mongo_query= mongo_collection.find_one({"user_id": user_id}, {'_id': 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user,
    # return {"user_details":user, "profile_picture":str(mongo_query)}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

