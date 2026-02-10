# Real-Time Speech Emotion Recognition

A real-time web application that recognizes emotions and state of mind through speech tone using machine learning.

## Features

- 🎤 **Real-time microphone recording** - Record directly from your browser
- 🧠 **Emotion detection** - Recognizes 7 emotions: Happy, Sad, Angry, Fear, Disgust, Neutral, Surprise
- 📊 **Confidence scores** - Shows probability for each emotion
- 🌐 **Web interface** - Easy-to-use browser-based UI
- ⚡ **Fast processing** - Real-time audio analysis

## Detected Emotions

- **Happy** - Joyful, pleased, cheerful
- **Sad** - Sorrowful, depressed, melancholic
- **Angry** - Furious, annoyed, hostile
- **Fear** - Anxious, worried, scared
- **Disgust** - Revulsion, distaste
- **Neutral** - Calm, balanced, normal
- **Surprise** - Shocked, amazed, astonished

## Technology Stack

- **Backend**: Python, FastAPI
- **ML/Audio**: TensorFlow, Librosa, Scikit-learn
- **Frontend**: HTML5, JavaScript, Web Audio API
- **Audio Features**: MFCCs, Pitch, Energy, Zero-crossing rate

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- FFmpeg (for audio format conversion)

**Install FFmpeg:**
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get install ffmpeg`
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd State-of-mind-recognition-
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the backend server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Click "Start Recording" and speak into your microphone

4. Click "Stop & Analyze" to get emotion predictions

## How It Works

1. **Audio Capture**: Browser captures audio from microphone using Web Audio API
2. **Feature Extraction**: Audio is processed to extract acoustic features (MFCCs, pitch, energy)
3. **Emotion Recognition**: Machine learning model analyzes features and predicts emotion
4. **Results Display**: Emotion probabilities are shown in real-time

## Project Structure

```
State-of-mind-recognition-/
├── backend/
│   ├── emotion_model.py      # ML model for emotion recognition
│   ├── audio_processor.py    # Audio feature extraction
│   └── api.py                # FastAPI endpoints
├── frontend/
│   ├── index.html            # Main web interface
│   ├── app.js                # Frontend logic
│   └── styles.css            # Styling
├── models/
│   └── emotion_classifier.py # Model training script
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## API Endpoints

- `GET /` - Serves the web interface
- `POST /predict-emotion` - Accepts audio data and returns emotion predictions
- `GET /emotions` - List supported emotions
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Options:

**Railway (Recommended - Easiest):**
```bash
railway login
railway init
railway up
```

**Render:**
- Connect GitHub repo at [render.com](https://render.com)
- Auto-deploys using `render.yaml`

**Vercel (Limited ML features):**
```bash
vercel --prod
```

**Note:** Vercel has package size limits. Use Railway or Render for full ML features.

## Future Enhancements

- [ ] Add WebSocket support for continuous streaming
- [ ] Support multiple languages
- [ ] Add voice stress analysis
- [ ] Mobile app version (React Native/Flutter)
- [ ] Save recording history
- [ ] Export emotion reports

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
