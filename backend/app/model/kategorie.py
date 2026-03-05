from pydantic import BaseModel

class Kategorie(BaseModel):
    id: str
    name: str
    aussagenpaare: list
