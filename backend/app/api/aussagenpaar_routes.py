from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aussagenpaar import Aussagenpaar
from app.db.mongo import db

router = APIRouter()

@router.post("/aussagenpaare")
async def create_aussagenpaar(aussagenpaar: Aussagenpaar):
    data = aussagenpaar.model_dump(exclude={"id"})
    result = await db["aussagenpaare"].insert_one(data)
    return {"id": str(result.inserted_id), **data}

@router.get("/aussagenpaare")
async def list_aussagenpaare():
    aussagenpaare = []
    async for doc in db["aussagenpaare"].find():
        aussagenpaare.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return aussagenpaare

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
    return {"id": aussagenpaar_id, **data}