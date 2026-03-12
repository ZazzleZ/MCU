from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.users_routes import router as users_router
from app.api.aussage_routes import router as aussage_router
from app.api.aussagenpaar_routes import router as aussagenpaar_router
from app.api.aufgabe_routes import router as aufgabe_router
from app.api.kategorie_routes import router as kategorie_router
from app.api.upload_routes import router as upload_routes

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
app.include_router(users_router)
app.include_router(aussage_router)
app.include_router(aussagenpaar_router)
app.include_router(aufgabe_router)
app.include_router(kategorie_router)
app.include_router(upload_routes)