from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routes import routers

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar routers (equivalente a registrar Blueprints)
for router in routers:
    app.include_router(router)

# Healthcheck
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Index
@app.get("/")
async def root():
    return FileResponse("static/index.html")
