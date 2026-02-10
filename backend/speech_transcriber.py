import whisper
import numpy as np
import tempfile
import os
from typing import Tuple, Optional


class SpeechTranscriber:
    """Transcribes speech using OpenAI Whisper."""

    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcriber.

        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
                       - tiny: fastest, least accurate
                       - base: good balance (recommended)
                       - small: better accuracy, slower
        """
        self.model_size = model_size
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the Whisper model (lazy loading)."""
        try:
            print(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size)
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None

    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Tuple[str, Optional[str]]:
        """
        Transcribe audio to text.

        Args:
            audio_data: Audio time series
            sample_rate: Sample rate of audio

        Returns:
            Tuple of (transcription_text, detected_language)
        """
        if self.model is None:
            self._load_model()
            if self.model is None:
                return "[Transcription unavailable - model not loaded]", None

        try:
            # Whisper expects 16kHz audio
            if sample_rate != 16000:
                import librosa
                audio_data = librosa.resample(
                    audio_data,
                    orig_sr=sample_rate,
                    target_sr=16000
                )

            # Ensure audio is float32 and normalized
            audio_data = audio_data.astype(np.float32)
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))

            # Transcribe
            result = self.model.transcribe(
                audio_data,
                fp16=False,  # Use FP32 for compatibility
                language="en",  # Force English (or set to None for auto-detect)
                task="transcribe"
            )

            transcription = result["text"].strip()
            language = result.get("language", "en")

            return transcription, language

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return f"[Transcription error: {str(e)}]", None

    def transcribe_from_file(self, audio_path: str) -> Tuple[str, Optional[str]]:
        """
        Transcribe audio from file path.

        Args:
            audio_path: Path to audio file

        Returns:
            Tuple of (transcription_text, detected_language)
        """
        if self.model is None:
            return "[Transcription unavailable]", None

        try:
            result = self.model.transcribe(audio_path)
            return result["text"].strip(), result.get("language", "en")
        except Exception as e:
            print(f"Error transcribing file: {e}")
            return f"[Transcription error: {str(e)}]", None
