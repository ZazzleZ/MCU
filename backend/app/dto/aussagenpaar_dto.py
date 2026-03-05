from pydantic import BaseModel


class AussagenpaarDTO(BaseModel):
    aussagen: list
    kategorie: list
    bearbeiter: str
    grafik_url: str
    kommentar: str

