# backend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["blog"]
collection = db["posts"]

class Post(BaseModel):
    title: str
    content: str

@app.post("/posts/", response_model=Post)
def create_post(post: Post):
    post_data = post.dict()
    post_id = collection.insert_one(post_data).inserted_id
    return {**post_data, "_id": str(post_id)}

@app.get("/posts/", response_model=List[Post])
def get_posts():
    posts_data = collection.find()
    return [Post(**post) for post in posts_data]

