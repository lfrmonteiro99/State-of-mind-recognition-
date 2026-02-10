import openai
import os
import tempfile
import numpy as np
import soundfile as sf
from typing import Tuple, Optional


class SpeechTranscriber:
    """Transcribes speech using OpenAI Whisper API (no local model needed)."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the transcriber.

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key

    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Tuple[str, Optional[str]]:
        """
        Transcribe audio to text using OpenAI API.

        Args:
            audio_data: Audio time series
            sample_rate: Sample rate of audio

        Returns:
            Tuple of (transcription_text, detected_language)
        """
        if not self.api_key:
            return "[Transcription unavailable - no OpenAI API key]", None

        try:
            # Save audio to temp file (OpenAI API requires file)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                sf.write(temp_path, audio_data, sample_rate)

            # Call OpenAI Whisper API
            with open(temp_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # or None for auto-detect
                )

            # Clean up temp file
            os.unlink(temp_path)

            transcription = transcript.get("text", "").strip()
            language = transcript.get("language", "en")

            if not transcription:
                transcription = "[No speech detected]"

            return transcription, language

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            # Clean up temp file if it exists
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass
            return f"[Transcription error: {str(e)}]", None

    def transcribe_from_file(self, audio_path: str) -> Tuple[str, Optional[str]]:
        """
        Transcribe audio from file path.

        Args:
            audio_path: Path to audio file

        Returns:
            Tuple of (transcription_text, detected_language)
        """
        if not self.api_key:
            return "[Transcription unavailable - no OpenAI API key]", None

        try:
            with open(audio_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )

            transcription = transcript.get("text", "").strip()
            language = transcript.get("language", "en")
            return transcription, language
        except Exception as e:
            print(f"Error transcribing file: {e}")
            return f"[Transcription error: {str(e)}]", None

