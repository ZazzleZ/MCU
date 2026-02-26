from pydantic import BaseModel
from datetime import datetime

class Aussage(BaseModel):
    id: str
    aussagenpaar_id: str
    aussage: str
    aenderungsdatum: datetime
    loesung: bool
