from fastapi import APIRouter
from model.user import User
from db.mongo import db

router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    result = await db["users"].insert_one(user.model_dump())
    return {"id": str(result.inserted_id), **user.model_dump()}
