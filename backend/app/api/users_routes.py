from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.user import User
from app.db.mongo import db

router = APIRouter()

def convert_objectid_to_str(data):
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@router.post("/users")
async def create_user(user: User):
    data = user.model_dump(exclude={"id"})
    result = await db["users"].insert_one(data)
    response = {"id": str(result.inserted_id), **data}
    return convert_objectid_to_str(response)

@router.get("/users")
async def list_users():
    users = []
    async for doc in db["users"].find():
        users.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return convert_objectid_to_str(users)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return None

@router.patch("/users/{user_id}")
async def update_user(user_id: str, user: User):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    data = user.model_dump(exclude={"id"})
    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    response = {"id": user_id, **data}
    return convert_objectid_to_str(response)