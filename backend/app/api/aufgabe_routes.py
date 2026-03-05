from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aufgabe import Aufgabe
from app.db.mongo import db

router = APIRouter()

@router.post("/aufgaben")
async def create_aufgabe(aufgabe: Aufgabe):
    data = aufgabe.model_dump(exclude={"id"})
    result = await db["aufgaben"].insert_one(data)
    return {"id": str(result.inserted_id), **data}
    

@router.get("/aufgaben")
async def list_aufgaben():
    aufgaben = []
    async for doc in db["aufgaben"].find():
        aufgaben.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return aufgaben

@router.delete("/aufgaben/{aufgabe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabe(aufgabe_id: str):
    if not ObjectId.is_valid(aufgabe_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["aufgaben"].delete_one({"_id": ObjectId(aufgabe_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Aufgabe nicht gefunden")
    return None

@router.patch("/aufgaben/{aufgabe_id}")
async def update_aufgabe(aufgabe_id: str, aufgabe: Aufgabe):
    if not ObjectId.is_valid(aufgabe_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    data = aufgabe.model_dump(exclude={"id"})
    result = await db["aufgaben"].update_one({"_id": ObjectId(aufgabe_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Aufgabe nicht gefunden")
    return {"id": aufgabe_id, **data}