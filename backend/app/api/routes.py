from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from model.user import User
from db.mongo import db

router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    result = await db["users"].insert_one(user.model_dump())
    return {"id": str(result.inserted_id), **user.model_dump()}
   
@router.get("/users")
async def list_users():
    users = []
    async for doc in db["users"].find():
        users.append({"id": str(doc["_id"]), "name": doc.get("name"), "email": doc.get("email")})
    return users

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    res = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return None
