from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.user import User
from app.db.mongo import db

router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    return "posted"
   
@router.get("/users")
async def list_users():
    users = []
    async for doc in db["users"].find():
        return "got"

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    return "deleted"
