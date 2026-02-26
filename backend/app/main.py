from api.routes import router
from fastapi import APIRouter
from bson import ObjectId
from db.mongo import db

router = APIRouter()

@router.post("/users/seed")
async def seed_demo_user():
    # Demo-User im gewünschten JSON-Format
    demo_user = {
        "id": str(ObjectId()),
        "email": "patrick@example.com",
        "password": "pass123",     # nur Demo! In echt: hash!
        "is_admin": False,
        "needs_pw_change": True
    }

    # Für MongoDB: id -> _id umwandeln
    to_insert = {**demo_user, "_id": ObjectId(demo_user["id"])}
    del to_insert["id"]

    await db["users"].insert_one(to_insert)

    # Response wieder im gewünschten JSON-Format (mit id)
    return demo_user