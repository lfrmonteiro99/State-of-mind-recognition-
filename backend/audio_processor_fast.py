import librosa
import numpy as np


class FastAudioProcessor:
    """Optimized audio processor with minimal feature extraction for faster processing."""

    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate

    def extract_features_fast(self, audio_data, sr=None):
        """
        Extract only essential audio features for faster processing.
        Reduces from 49 features to ~20 for 2-3x speedup.

        Args:
            audio_data: Audio time series
            sr: Sample rate (uses default if None)

        Returns:
            numpy array of extracted features
        """
        if sr is None:
            sr = self.sample_rate

        features = []

        # 1. MFCC (reduced from 13 to 8) - most important for emotion
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=8, n_fft=1024, hop_length=512)
        features.extend(np.mean(mfccs, axis=1))
        features.extend(np.std(mfccs, axis=1))

        # 2. RMS Energy - loudness (critical for emotion)
        rms = librosa.feature.rms(y=audio_data, frame_length=1024, hop_length=512)
        features.append(np.mean(rms))
        features.append(np.std(rms))

        # 3. Zero Crossing Rate - measure of noisiness
        zcr = librosa.feature.zero_crossing_rate(audio_data, frame_length=1024, hop_length=512)
        features.append(np.mean(zcr))

        # 4. Spectral Centroid - brightness of sound
        spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr, n_fft=1024, hop_length=512)
        features.append(np.mean(spectral_centroid))

        return np.array(features)

    def preprocess_audio(self, audio_data, sr=None):
        """
        Preprocess raw audio data (optimized version).

        Args:
            audio_data: Raw audio time series
            sr: Sample rate

        Returns:
            Preprocessed audio data
        """
        if sr is None:
            sr = self.sample_rate

        # Normalize audio
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val

        # Simple trim (faster than librosa.effects.trim)
        # Remove leading/trailing silence
        threshold = 0.01
        non_silent = np.abs(audio_data) > threshold
        if np.any(non_silent):
            start = np.argmax(non_silent)
            end = len(audio_data) - np.argmax(non_silent[::-1])
            audio_data = audio_data[start:end]

        return audio_data

    def process_audio_buffer(self, audio_buffer, original_sr=None):
        """
        Process audio buffer from browser and extract features (optimized).

        Args:
            audio_buffer: Audio data buffer
            original_sr: Original sample rate

        Returns:
            Feature vector
        """
        # Resample if needed
        if original_sr and original_sr != self.sample_rate:
            audio_data = librosa.resample(
                audio_buffer,
                orig_sr=original_sr,
                target_sr=self.sample_rate,
                res_type='kaiser_fast'  # Faster resampling
            )
        else:
            audio_data = audio_buffer

        # Preprocess
        audio_data = self.preprocess_audio(audio_data)

        # Extract features (fast version)
        features = self.extract_features_fast(audio_data)

        return features
