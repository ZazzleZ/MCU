from pydantic import BaseModel


class AufgabeDTO(BaseModel):
    aufgabenname: str
    aussagenpaare: list
    is_klausur: bool

