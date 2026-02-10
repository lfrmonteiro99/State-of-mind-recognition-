from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import io
import soundfile as sf
from pydub import AudioSegment
import tempfile
import os

from backend.audio_processor import AudioProcessor
from backend.emotion_model import EmotionRecognizer


app = FastAPI(title="Speech Emotion Recognition API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
audio_processor = AudioProcessor()
emotion_recognizer = EmotionRecognizer()
emotion_recognizer.create_simple_demo_model()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Speech Emotion Recognition API",
        "version": "1.0.0"
    }


@app.post("/predict-emotion")
async def predict_emotion(audio: UploadFile = File(...)):
    """
    Predict emotion from uploaded audio file.

    Args:
        audio: Audio file (WAV, MP3, etc.)

    Returns:
        Emotion predictions with probabilities
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()

        # Try to detect and convert audio format
        audio_data, sample_rate = None, None

        try:
            # First, try direct reading with soundfile (WAV, FLAC, OGG)
            audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))
        except (sf.LibsndfileError, RuntimeError):
            # If that fails, use pydub to convert from WebM/other formats
            try:
                # Detect format from content (WebM is common from browsers)
                audio_segment = AudioSegment.from_file(
                    io.BytesIO(audio_bytes),
                    format="webm"
                )

                # Convert to WAV in memory
                wav_io = io.BytesIO()
                audio_segment.export(wav_io, format="wav")
                wav_io.seek(0)

                # Now read with soundfile
                audio_data, sample_rate = sf.read(wav_io)

            except Exception as e:
                # Try without specifying format (let pydub detect)
                try:
                    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
                    wav_io = io.BytesIO()
                    audio_segment.export(wav_io, format="wav")
                    wav_io.seek(0)
                    audio_data, sample_rate = sf.read(wav_io)
                except Exception as final_error:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported audio format. Please ensure microphone recording is working. Error: {str(final_error)}"
                    )

        # Handle stereo audio (convert to mono)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Validate audio data
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")

        if len(audio_data) < sample_rate * 0.5:  # Less than 0.5 seconds
            raise HTTPException(
                status_code=400,
                detail="Audio too short. Please record at least 1 second of speech."
            )

        # Process audio and extract features
        features = audio_processor.process_audio_buffer(audio_data, sample_rate)

        # Predict emotion
        predictions = emotion_recognizer.predict_emotion(features)

        return JSONResponse(content={
            "success": True,
            "data": predictions,
            "audio_duration": len(audio_data) / sample_rate,
            "sample_rate": sample_rate
        })

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )


@app.get("/emotions")
async def get_emotions():
    """Get list of supported emotions."""
    return {
        "emotions": emotion_recognizer.emotions,
        "count": len(emotion_recognizer.emotions)
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "model_loaded": emotion_recognizer.is_trained,
        "supported_emotions": emotion_recognizer.emotions
    }
