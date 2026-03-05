from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.kategorie import Kategorie
from app.db.mongo import db

router = APIRouter()

@router.post("/kategorien")
async def create_kategorie(kategorie: Kategorie):
    data = kategorie.model_dump(exclude={"id"})
    result = await db["kategorien"].insert_one(data)
    return {"id": str(result.inserted_id), **data}

@router.get("/kategorien")
async def list_kategorien():
    kategorien = []
    async for doc in db["kategorien"].find():
        kategorien.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return kategorien

@router.delete("/kategorien/{kategorie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategorie(kategorie_id: str):
    if not ObjectId.is_valid(kategorie_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["kategorien"].delete_one({"_id": ObjectId(kategorie_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    return None
