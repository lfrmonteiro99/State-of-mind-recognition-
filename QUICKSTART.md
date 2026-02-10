# Quick Start Guide

Get your Speech Emotion Recognition app up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- **FFmpeg** installed (required for audio format conversion)
- Microphone connected to your computer
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add to PATH environment variable

Or use Chocolatey:
```bash
choco install ffmpeg
```

## Installation Steps

### 1. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

You should see:
```
🎤 Speech Emotion Recognition Server
====================================
✅ Server starting...
🌐 Open your browser and go to: http://localhost:8000
```

### 3. Open the Web App

Open your browser and navigate to:
```
http://localhost:8000
```

## How to Use

1. **Click "Start Recording"**
   - Your browser will ask for microphone permission
   - Click "Allow" to grant access

2. **Speak Naturally**
   - Talk for at least 2-3 seconds
   - Express how you're feeling!
   - You'll see a real-time audio visualizer

3. **Click "Stop & Analyze"**
   - The app processes your speech
   - Results appear in seconds

4. **View Results**
   - See your top detected emotion
   - View confidence scores for all emotions
   - Try again with different tones!

## Troubleshooting

### Microphone Not Working

**Problem:** Browser doesn't show microphone permission prompt

**Solution:**
- Ensure you're using HTTPS or localhost
- Check browser settings: Settings → Privacy → Microphone
- Try a different browser

### Installation Errors

**Problem:** `pip install` fails

**Solution:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

**Problem:** librosa installation fails on Windows

**Solution:**
```bash
# Install Visual C++ Build Tools first, then:
pip install librosa --no-cache-dir
```

### Server Won't Start

**Problem:** Port 8000 already in use

**Solution:**
Edit `main.py` and change the port:
```python
uvicorn.run(..., port=8001)  # Use different port
```

## What Emotions Are Detected?

- 😊 **Happy** - Joyful, cheerful, pleased
- 😢 **Sad** - Sorrowful, melancholic, down
- 😠 **Angry** - Furious, annoyed, frustrated
- 😨 **Fear** - Anxious, scared, worried
- 🤢 **Disgust** - Revulsion, distaste
- 😐 **Neutral** - Calm, balanced, normal
- 😲 **Surprise** - Shocked, amazed, astonished

## Tips for Better Results

1. **Speak Clearly** - Enunciate your words
2. **Record 3-5 seconds** - Gives more data to analyze
3. **Express Emotion** - Let your feelings show in your tone
4. **Quiet Environment** - Reduce background noise
5. **Try Different Emotions** - Test various emotional states

## Advanced: Training Your Own Model

The current app uses a demo model with heuristics. For production use, train on real datasets:

```bash
# Download RAVDESS dataset first
# https://zenodo.org/record/1188976

# Train model
python models/train_model.py --data_path /path/to/RAVDESS

# The trained model will be saved and automatically used
```

## API Documentation

Access interactive API docs at:
```
http://localhost:8000/docs
```

### API Endpoints

**POST /predict-emotion**
- Upload audio file
- Returns emotion predictions

**GET /emotions**
- List supported emotions

**GET /health**
- Check server status

## Next Steps

- ✅ Test the app with different emotions
- ✅ Try recording in different situations
- ✅ Train a custom model on real datasets
- ✅ Deploy to production (see deployment guide)
- ✅ Integrate into your own applications

## Need Help?

- Check the main README.md for detailed documentation
- Review the code in backend/ and frontend/ directories
- Open an issue on GitHub

## Stop the Server

Press `Ctrl+C` in the terminal running the server.

---

**Enjoy analyzing emotions! 🎤🧠**
