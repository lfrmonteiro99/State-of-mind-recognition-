import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


class EmotionRecognizer:
    """Machine learning model for emotion recognition from speech."""

    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False

    def create_model(self):
        """Create a Random Forest classifier for emotion recognition."""
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        return self.model

    def create_simple_demo_model(self):
        """
        Create a simple rule-based demo model for testing.
        This should be replaced with a trained model for production.
        """
        self.is_trained = True

    def predict_emotion(self, features):
        """
        Predict emotion from audio features.

        Args:
            features: Extracted audio features (numpy array)

        Returns:
            dict: Emotion predictions with probabilities
        """
        # Ensure features is 2D array
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # For demo: Use simple heuristics based on features
        # In production, replace with trained model
        predictions = self._demo_predict(features[0])

        return predictions

    def _demo_predict(self, features):
        """
        Demo prediction using simple heuristics.
        Replace with actual model.predict_proba() when trained.
        """
        # Simple heuristic based on acoustic features
        # Features approximate indices (based on audio_processor.py):
        # 0-12: MFCC means
        # 13-25: MFCC stds
        # 26-37: Chroma means
        # 38-39: Spectral centroid mean/std
        # 40: Spectral rolloff
        # 41: Spectral bandwidth
        # 42-43: ZCR mean/std
        # 44-45: RMS mean/std
        # 46-47: Pitch mean/std
        # 48: Tempo

        probabilities = np.zeros(len(self.emotions))

        if len(features) < 40:
            # Fallback if features incomplete
            probabilities[4] = 1.0  # neutral
            return self._format_predictions(probabilities)

        # Energy/loudness indicators (RMS)
        energy = features[44] if len(features) > 44 else 0.1
        energy_std = features[45] if len(features) > 45 else 0.05

        # Pitch indicators
        pitch_mean = features[46] if len(features) > 46 else 150
        pitch_std = features[47] if len(features) > 47 else 20

        # Spectral indicators
        spectral_centroid = features[38] if len(features) > 38 else 1000
        zcr = features[42] if len(features) > 42 else 0.1

        # Tempo
        tempo = features[48] if len(features) > 48 else 120

        # Simple rule-based classification for demo
        # High energy + high pitch variance = angry
        if energy > 0.15 and pitch_std > 30:
            probabilities[0] = 0.6  # angry
            probabilities[6] = 0.2  # surprise
            probabilities[4] = 0.2  # neutral

        # Low energy + low pitch = sad
        elif energy < 0.08 and pitch_mean < 180:
            probabilities[5] = 0.7  # sad
            probabilities[4] = 0.2  # neutral
            probabilities[2] = 0.1  # fear

        # High pitch + moderate energy = happy
        elif pitch_mean > 200 and energy > 0.1:
            probabilities[3] = 0.6  # happy
            probabilities[6] = 0.2  # surprise
            probabilities[4] = 0.2  # neutral

        # High ZCR + variable pitch = fear
        elif zcr > 0.15 and pitch_std > 25:
            probabilities[2] = 0.5  # fear
            probabilities[6] = 0.3  # surprise
            probabilities[4] = 0.2  # neutral

        # Fast tempo + high energy = surprise/happy
        elif tempo > 140 and energy > 0.12:
            probabilities[6] = 0.5  # surprise
            probabilities[3] = 0.3  # happy
            probabilities[4] = 0.2  # neutral

        # Default to neutral with some variation
        else:
            probabilities[4] = 0.5  # neutral
            probabilities[3] = 0.2  # happy
            probabilities[5] = 0.15  # sad
            probabilities[0] = 0.15  # angry

        # Normalize to ensure sum = 1
        probabilities = probabilities / probabilities.sum()

        return self._format_predictions(probabilities)

    def _format_predictions(self, probabilities):
        """Format predictions as dictionary with emotion labels."""
        results = {
            'predictions': {},
            'top_emotion': '',
            'confidence': 0.0
        }

        for i, emotion in enumerate(self.emotions):
            results['predictions'][emotion] = float(probabilities[i])

        # Get top emotion
        top_idx = np.argmax(probabilities)
        results['top_emotion'] = self.emotions[top_idx]
        results['confidence'] = float(probabilities[top_idx])

        return results

    def train(self, X_train, y_train):
        """
        Train the emotion recognition model.

        Args:
            X_train: Training features
            y_train: Training labels
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)

        # Create and train model
        self.create_model()
        self.model.fit(X_scaled, y_train)
        self.is_trained = True

        return self.model

    def save_model(self, filepath):
        """Save trained model to disk."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'emotions': self.emotions,
            'is_trained': self.is_trained
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filepath):
        """Load trained model from disk."""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)

            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.emotions = model_data['emotions']
            self.is_trained = model_data['is_trained']
            return True
        return False
