from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.kategorie import Kategorie
from app.db.mongo import db

router = APIRouter()

@router.post("/kategorien")
async def create_kategorie(kategorie: Kategorie):
    return "posted"

@router.get("/kategorien")
async def list_kategorien():
    return "got"

@router.delete("/kategorien/{kategorie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategorie(kategorie_id: str):
    return "deleted"
