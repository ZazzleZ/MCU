from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aufgabe import Aufgabe
from app.db.mongo import db

router = APIRouter()

router.post("/aufgaben")
async def create_aufgabe(aufgabe: Aufgabe):
    return "posted"

router.get("/aufgaben")
async def list_aufgaben():
    return "got"

router.delete("/aufgaben/{aufgabe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabe(aufgabe_id: str):
    return "deleted"
