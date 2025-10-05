import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base, get_db
from dotenv import load_dotenv
from routes import auth, requests, inventory

load_dotenv()

app = FastAPI(title="ICT Ticketing System API")

# allow frontend (you may lock this down to your frontend origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, set to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# include routers with /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])

@app.on_event("startup")
def on_startup():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return FileResponse("frontend/ict.html")
