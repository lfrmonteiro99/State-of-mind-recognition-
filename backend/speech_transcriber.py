from faster_whisper import WhisperModel
import numpy as np
import tempfile
import os
from typing import Tuple, Optional


class SpeechTranscriber:
    """Transcribes speech using faster-whisper (optimized OpenAI Whisper)."""

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
            print(f"Loading faster-whisper {self.model_size} model...")
            # Use CPU for compatibility, int8 for speed/memory
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
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
            # faster-whisper expects 16kHz audio
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

            # Transcribe - faster-whisper returns segments
            segments, info = self.model.transcribe(
                audio_data,
                language="en",  # Force English (or None for auto-detect)
                task="transcribe",
                beam_size=5,
                vad_filter=True  # Voice activity detection
            )

            # Combine all segments
            transcription = " ".join([segment.text for segment in segments]).strip()
            language = info.language if hasattr(info, 'language') else "en"

            if not transcription:
                transcription = "[No speech detected]"

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
            segments, info = self.model.transcribe(audio_path, language="en")
            transcription = " ".join([segment.text for segment in segments]).strip()
            language = info.language if hasattr(info, 'language') else "en"
            return transcription, language
        except Exception as e:
            print(f"Error transcribing file: {e}")
            return f"[Transcription error: {str(e)}]", None
