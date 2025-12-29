"""
Vercel Serverless Function Entry Point

NOTE: This is a simplified version for Vercel deployment.
Due to package size limitations, we use lightweight dependencies.
For full ML features, deploy to Railway, Render, or Google Cloud Run instead.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import io
import json
import os

app = FastAPI(title="Speech Emotion Recognition API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple emotion predictor without heavy ML dependencies
class SimplifiedEmotionPredictor:
    """Lightweight emotion prediction for Vercel deployment."""

    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    def predict(self, audio_data):
        """
        Simplified prediction based on basic audio properties.
        For production, use the full deployment on Railway/Render.
        """
        # Simple heuristic based on audio amplitude and variance
        mean_amplitude = np.mean(np.abs(audio_data))
        variance = np.var(audio_data)

        probabilities = np.zeros(len(self.emotions))

        # Very simple rules (replace with actual ML model in full deployment)
        if mean_amplitude > 0.15 and variance > 0.02:
            probabilities[0] = 0.6  # angry
            probabilities[6] = 0.2  # surprise
            probabilities[4] = 0.2  # neutral
        elif mean_amplitude < 0.08:
            probabilities[5] = 0.7  # sad
            probabilities[4] = 0.3  # neutral
        elif variance > 0.03:
            probabilities[3] = 0.6  # happy
            probabilities[6] = 0.4  # surprise
        else:
            probabilities[4] = 0.5  # neutral
            probabilities[3] = 0.3  # happy
            probabilities[5] = 0.2  # sad

        probabilities = probabilities / probabilities.sum()

        top_idx = np.argmax(probabilities)

        return {
            'predictions': {emotion: float(prob) for emotion, prob in zip(self.emotions, probabilities)},
            'top_emotion': self.emotions[top_idx],
            'confidence': float(probabilities[top_idx])
        }


predictor = SimplifiedEmotionPredictor()


@app.get("/")
async def serve_frontend():
    """Serve the main HTML page."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Speech Emotion Recognition API", "status": "online"}


@app.get("/api")
@app.get("/api/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Speech Emotion Recognition API (Vercel Deployment)",
        "version": "1.0.0",
        "note": "Simplified version - for full ML features, use Railway/Render deployment"
    }


@app.post("/api/predict-emotion")
async def predict_emotion(audio: UploadFile = File(...)):
    """
    Predict emotion from uploaded audio file.
    Simplified version for Vercel serverless constraints.
    """
    try:
        # Read audio bytes
        audio_bytes = await audio.read()

        # Convert to numpy array (simplified - assumes WAV format)
        # In production, use soundfile or librosa
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_data = audio_array.astype(np.float32) / 32768.0  # Normalize

        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")

        # Predict emotion
        predictions = predictor.predict(audio_data)

        return JSONResponse(content={
            "success": True,
            "data": predictions,
            "audio_duration": len(audio_data) / 16000,  # Assuming 16kHz
            "note": "Using simplified model - deploy to Railway/Render for full ML features"
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )


@app.get("/api/emotions")
async def get_emotions():
    """Get list of supported emotions."""
    return {
        "emotions": predictor.emotions,
        "count": len(predictor.emotions)
    }


@app.get("/api/health")
async def health_check():
    """Health check."""
    return {
        "status": "healthy",
        "deployment": "Vercel Serverless",
        "supported_emotions": predictor.emotions
    }


# Export for Vercel
handler = app
