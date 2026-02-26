from pydantic import BaseModel

class Aussagenpaar(BaseModel):
    id: str
    aussagen: list
    kategorie: list
    bearbeiter: str
    grafik_url: str
    kommentar: str
