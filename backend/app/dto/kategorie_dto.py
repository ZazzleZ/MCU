from pydantic import BaseModel


class KategorieDTO(BaseModel):
    name: str
    aussagenpaare: list

