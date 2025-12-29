"""
Model Training Script for Speech Emotion Recognition

This script trains a machine learning model on emotion-labeled speech datasets.
Currently configured for RAVDESS, TESS, and CREMA-D datasets.

Usage:
    python models/train_model.py --data_path /path/to/dataset
"""

import os
import sys
import numpy as np
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_processor import AudioProcessor
from backend.emotion_model import EmotionRecognizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import librosa


class ModelTrainer:
    """Handles training of emotion recognition models."""

    def __init__(self, data_path):
        self.data_path = data_path
        self.audio_processor = AudioProcessor()
        self.emotion_recognizer = EmotionRecognizer()

    def load_ravdess_dataset(self):
        """
        Load RAVDESS dataset.

        RAVDESS filename format: 03-01-06-01-02-01-12.wav
        - Modality (01 = full-AV, 02 = video-only, 03 = audio-only)
        - Vocal channel (01 = speech, 02 = song)
        - Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised)
        - Emotional intensity (01 = normal, 02 = strong)
        - Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door")
        - Repetition (01 = 1st, 02 = 2nd)
        - Actor (01 to 24)
        """
        emotion_map = {
            '01': 'neutral',
            '02': 'neutral',  # calm -> neutral
            '03': 'happy',
            '04': 'sad',
            '05': 'angry',
            '06': 'fear',
            '07': 'disgust',
            '08': 'surprise'
        }

        features = []
        labels = []

        audio_files = list(Path(self.data_path).rglob('*.wav'))

        print(f"Found {len(audio_files)} audio files")

        for i, file_path in enumerate(audio_files):
            if i % 100 == 0:
                print(f"Processing {i}/{len(audio_files)}...")

            try:
                # Extract emotion from filename
                parts = file_path.stem.split('-')
                if len(parts) >= 3:
                    emotion_code = parts[2]
                    emotion = emotion_map.get(emotion_code)

                    if emotion:
                        # Load and process audio
                        audio_data, sr = librosa.load(str(file_path), sr=22050)

                        # Extract features
                        feature_vector = self.audio_processor.process_audio_buffer(audio_data, sr)

                        features.append(feature_vector)
                        labels.append(emotion)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

        return np.array(features), np.array(labels)

    def train(self, X, y):
        """Train the emotion recognition model."""
        print("\n" + "="*60)
        print("Training Emotion Recognition Model")
        print("="*60)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\nTraining samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        print(f"Feature dimensions: {X_train.shape[1]}")

        # Train model
        print("\nTraining model...")
        self.emotion_recognizer.train(X_train, y_train)

        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.emotion_recognizer.model.predict(
            self.emotion_recognizer.scaler.transform(X_test)
        )

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        # Calculate accuracy
        accuracy = np.mean(y_pred == y_test)
        print(f"\nOverall Accuracy: {accuracy*100:.2f}%")

        return accuracy

    def save_model(self, output_path='models/emotion_model.pkl'):
        """Save trained model."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.emotion_recognizer.save_model(output_path)
        print(f"\nModel saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Train emotion recognition model')
    parser.add_argument('--data_path', type=str, required=True,
                        help='Path to dataset directory')
    parser.add_argument('--output', type=str, default='models/emotion_model.pkl',
                        help='Output path for trained model')

    args = parser.parse_args()

    # Initialize trainer
    trainer = ModelTrainer(args.data_path)

    # Load dataset
    print("Loading dataset...")
    X, y = trainer.load_ravdess_dataset()

    if len(X) == 0:
        print("No data loaded. Please check your dataset path.")
        return

    print(f"Loaded {len(X)} samples")

    # Train model
    accuracy = trainer.train(X, y)

    # Save model
    trainer.save_model(args.output)

    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
