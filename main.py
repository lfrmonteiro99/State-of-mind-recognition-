import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.api import app

# Serve static frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

# Mount static files
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse(os.path.join(frontend_path, "index.html"))


if __name__ == "__main__":
    print("=" * 60)
    print("🎤 Speech Emotion Recognition Server")
    print("=" * 60)
    print("\n✅ Server starting...")
    print(f"🌐 Open your browser and go to: http://localhost:8000")
    print(f"📡 API docs available at: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the server\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
