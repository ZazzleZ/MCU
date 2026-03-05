from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aussage import Aussage
from app.db.mongo import db

router = APIRouter()

@router.post("/aussagen")
async def create_aussage(aussage: Aussage):
    data = aussage.model_dump(exclude={"id"})
    result = await db["aussagen"].insert_one(data)
    return {"id": str(result.inserted_id), **data}

@router.get("/aussagen")
async def list_aussagen():
    aussagen = []
    async for doc in db["aussagen"].find():
        aussagen.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return aussagen

@router.delete("/aussagen/{aussage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aussage(aussage_id: str):
    if not ObjectId.is_valid(aussage_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["aussagen"].delete_one({"_id": ObjectId(aussage_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Aussage nicht gefunden")
    return None

@router.patch("/aussagen/{aussage_id}")
async def update_aussage(aussage_id: str, aussage: Aussage):
    if not ObjectId.is_valid(aussage_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    data = aussage.model_dump(exclude={"id"})
    result = await db["aussagen"].update_one({"_id": ObjectId(aussage_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Aussage nicht gefunden")
    return {"id": aussage_id, **data}