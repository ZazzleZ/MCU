from pydantic import BaseModel

class Aufgabe(BaseModel):
    id: str
    aufgabenname: str
    aussagenpaare: list
    is_klausur: bool
