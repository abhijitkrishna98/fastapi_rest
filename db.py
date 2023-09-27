from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost/fastapi-rest"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["fastapi-rest"]
mongo_collection = mongo_db["fastapi"]