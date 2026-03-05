from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.dto.kategorie_dto import KategorieDTO
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

@router.post("/kategorien")
async def create_kategorie(kategorie: KategorieDTO):
    data = kategorie.model_dump(exclude={"id"})
    result = await db["kategorien"].insert_one(data)
    response = {"id": str(result.inserted_id), **data}
    return convert_objectid_to_str(response)

@router.get("/kategorien")
async def list_kategorien():
    kategorien = []
    async for doc in db["kategorien"].find():
        kategorien.append({"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}})
    return convert_objectid_to_str(kategorien)

@router.delete("/kategorien/{kategorie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategorie(kategorie_id: str):
    if not ObjectId.is_valid(kategorie_id):
        raise HTTPException(status_code=400, detail="Ungültige ID")
    result = await db["kategorien"].delete_one({"_id": ObjectId(kategorie_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    return None
