from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aussagenpaar import Aussagenpaar
from app.db.mongo import db

router = APIRouter()

router.post("/aussagenpaare")
async def create_aussagenpaar(aussagenpaar: Aussagenpaar):
    return "posted"

router.get("/aussagenpaare")
async def list_aussagenpaare():
    return "got"

router.delete("/aussagenpaare/{aussagenpaar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aussagenpaar(aussagenpaar_id: str):
    return "deleted"
