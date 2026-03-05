from datetime import datetime
from turtle import st

from pydantic import BaseModel


class AussageDTO(BaseModel):
    aussagenpaar_id: str
    aussage: str
    aenderungsdatum: datetime
    loesung: bool

