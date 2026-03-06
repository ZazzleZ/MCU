from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.dto.aussagenpaar_dto import AussagenpaarDTO
from app.model.aussagenpaar import Aussagenpaar
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

@router.post("/aussagenpaare")
async def create_aussagenpaar(aussagenpaar: AussagenpaarDTO):
    data = aussagenpaar.model_dump(exclude={"id"})
    result = await db["aussagenpaare"].insert_one(data)
    response = {"id": str(result.inserted_id), **data}
    return convert_objectid_to_str(response)

@router.get("/aussagenpaare")
async def list_aussagenpaare():
    aussagenpaare = []
    async for doc in db["aussagenpaare"].find():
        aussagenpaare.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return convert_objectid_to_str(aussagenpaare)

@router.get("/aussagenpaare/{aussagenpaar_id}")
async def get_aussagenpaar(aussagenpaar_id: str):
    if not ObjectId.is_valid(aussagenpaar_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    doc = await db["aussagenpaare"].find_one({"_id": ObjectId(aussagenpaar_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Aussagenpaar nicht gefunden")
    response = {"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}}
    return convert_objectid_to_str(response)

@router.delete("/aussagenpaare/{aussagenpaar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aussagenpaar(aussagenpaar_id: str):
    if not ObjectId.is_valid(aussagenpaar_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["aussagenpaare"].delete_one({"_id": ObjectId(aussagenpaar_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Aussagenpaar nicht gefunden")
    return None

@router.patch("/aussagenpaare/{aussagenpaar_id}")
async def update_aussagenpaar(aussagenpaar_id: str, aussagenpaar: Aussagenpaar):
    if not ObjectId.is_valid(aussagenpaar_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    data = aussagenpaar.model_dump(exclude={"id"})
    result = await db["aussagenpaare"].update_one({"_id": ObjectId(aussagenpaar_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Aussagenpaar nicht gefunden")
    response = {"id": aussagenpaar_id, **data}
    return convert_objectid_to_str(response)
