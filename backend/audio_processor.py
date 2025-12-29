import librosa
import numpy as np
from scipy import signal


class AudioProcessor:
    """Processes audio data and extracts features for emotion recognition."""

    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate

    def extract_features(self, audio_data, sr=None):
        """
        Extract comprehensive audio features for emotion recognition.

        Args:
            audio_data: Audio time series
            sr: Sample rate (uses default if None)

        Returns:
            numpy array of extracted features
        """
        if sr is None:
            sr = self.sample_rate

        features = []

        # 1. MFCC (Mel-Frequency Cepstral Coefficients) - captures timbre
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)
        features.extend(mfcc_mean)
        features.extend(mfcc_std)

        # 2. Chroma features - pitch class profiles
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        features.extend(chroma_mean)

        # 3. Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
        features.append(np.mean(spectral_centroid))
        features.append(np.std(spectral_centroid))

        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)
        features.append(np.mean(spectral_rolloff))

        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)
        features.append(np.mean(spectral_bandwidth))

        # 4. Zero Crossing Rate - measure of noisiness
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        features.append(np.mean(zcr))
        features.append(np.std(zcr))

        # 5. RMS Energy - loudness
        rms = librosa.feature.rms(y=audio_data)
        features.append(np.mean(rms))
        features.append(np.std(rms))

        # 6. Pitch features
        try:
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)

            if len(pitch_values) > 0:
                features.append(np.mean(pitch_values))
                features.append(np.std(pitch_values))
            else:
                features.extend([0, 0])
        except:
            features.extend([0, 0])

        # 7. Tempo
        try:
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
            features.append(tempo)
        except:
            features.append(0)

        return np.array(features)

    def preprocess_audio(self, audio_data, sr=None):
        """
        Preprocess raw audio data.

        Args:
            audio_data: Raw audio time series
            sr: Sample rate

        Returns:
            Preprocessed audio data
        """
        if sr is None:
            sr = self.sample_rate

        # Normalize audio
        audio_data = audio_data / np.max(np.abs(audio_data) + 1e-6)

        # Remove silence from beginning and end
        audio_data, _ = librosa.effects.trim(audio_data, top_db=20)

        return audio_data

    def process_audio_buffer(self, audio_buffer, original_sr=None):
        """
        Process audio buffer from browser and extract features.

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
                target_sr=self.sample_rate
            )
        else:
            audio_data = audio_buffer

        # Preprocess
        audio_data = self.preprocess_audio(audio_data)

        # Extract features
        features = self.extract_features(audio_data)

        return features
