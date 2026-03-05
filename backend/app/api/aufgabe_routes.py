from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.dto.aufgabe_dto import AufgabeDTO
from app.model.aufgabe import Aufgabe
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

@router.post("/aufgaben")
async def create_aufgabe(aufgabe: AufgabeDTO):
    data = aufgabe.model_dump(exclude={"id"})
    result = await db["aufgaben"].insert_one(data)
    response = {"id": str(result.inserted_id), **data}
    return convert_objectid_to_str(response)
    
@router.get("/aufgaben")
async def list_aufgaben():
    aufgaben = []
    async for doc in db["aufgaben"].find():
        aufgaben.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return convert_objectid_to_str(aufgaben)

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
    response =  {"id": aufgabe_id, **data}
    return convert_objectid_to_str(response)
