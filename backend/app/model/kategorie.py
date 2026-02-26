from pydantic import BaseModel

class Kategorie(BaseModel):
    id: str
    aussagenpaare: list
