from fastapi import FastAPI
from app.api.users_routes import router as users_router
from app.api.aussage_routes import router as aussage_router
from app.api.aussagenpaar_routes import router as aussagenpaar_router
from app.api.aufgabe_routes import router as aufgabe_router
from app.api.kategorie_routes import router as kategorie_router

app = FastAPI()

app.include_router(users_router)
app.include_router(aussage_router)
app.include_router(aussagenpaar_router)
app.include_router(aufgabe_router)
app.include_router(kategorie_router)
