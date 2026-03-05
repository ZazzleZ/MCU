from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.model.aussage import Aussage
from app.db.mongo import db

router = APIRouter()

router.post("/aussagen")
async def create_aussage(aussage: Aussage):
    return "posted"

router.get("/aussagen")
async def list_aussagen():
    return "got"

router.delete("/aussagen/{aussage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aussage(aussage_id: str):
    return "deleted"
