import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import auth, tasks

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple task management REST API with JWT authentication",
    version="1.0.0",
)

# CORS - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Serve frontend static files
# Works in both local dev (3 dirs up) and Docker (2 dirs up)
_app_dir = os.path.dirname(os.path.abspath(__file__))
_candidates = [
    os.path.normpath(os.path.join(_app_dir, "..", "..", "frontend")),
    os.path.normpath(os.path.join(_app_dir, "..", "..", "..", "frontend")),
]
frontend_dir = next((c for c in _candidates if os.path.exists(c)), None)

if frontend_dir:
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        """Serve the frontend HTML page."""
        return FileResponse(os.path.join(frontend_dir, "index.html"))
