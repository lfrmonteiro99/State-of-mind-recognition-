# Deployment Guide

This guide covers deploying your Speech Emotion Recognition app to various platforms.

## ⚠️ Important: Vercel Limitations

**Vercel has significant limitations for this app:**
- 250MB deployment size limit (our ML dependencies exceed this)
- 50MB function size limit
- Limited execution time (10-60s)
- Cold starts with ML libraries are slow

**Recommendation:** Use Railway, Render, or Google Cloud Run for the full ML experience.

---

## 🚂 Option 1: Railway (Recommended - Easiest)

Railway is perfect for this app with no configuration needed!

### Steps:

1. **Install Railway CLI** (optional):
```bash
npm install -g @railway/cli
railway login
```

2. **Deploy via GitHub** (easier):
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys!

3. **Or deploy via CLI**:
```bash
railway init
railway up
```

4. **Set environment (if needed)**:
   - Railway auto-detects `railway.json`
   - No environment variables needed for basic setup

5. **Get your URL**:
   - Railway provides a public URL automatically
   - Click "Generate Domain" in Railway dashboard

### Cost:
- Free tier: $5 credit/month
- Starter: $5/month
- Perfect for this app!

---

## 🎨 Option 2: Render (Also Great)

Render offers generous free tier with persistent deployment.

### Steps:

1. **Go to [render.com](https://render.com)**

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects `render.yaml`

3. **Configure** (if not using render.yaml):
   - **Name**: speech-emotion-recognition
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free or Starter

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for build (~5-10 minutes first time)

5. **Access your app**:
   - Render provides: `https://speech-emotion-recognition.onrender.com`

### Cost:
- Free tier: Available (sleeps after inactivity)
- Starter: $7/month (always on)

---

## 🌐 Option 3: Google Cloud Run (Scalable)

Best for production and high traffic.

### Steps:

1. **Create Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
ENV PORT=8080
EXPOSE 8080

# Run app
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Install Google Cloud CLI**:
```bash
gcloud init
gcloud auth login
```

3. **Deploy**:
```bash
gcloud run deploy speech-emotion-recognition \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

4. **Access**:
   - Cloud Run provides a URL
   - Auto-scales based on traffic

### Cost:
- Free tier: 2 million requests/month
- Pay per use after that
- Sleeps when not in use (cost-effective)

---

## 🔵 Option 4: Vercel (Limited)

**Warning:** Vercel deployment uses a **simplified model** without full ML features due to size constraints.

### Steps:

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
vercel
```

3. **Configure**:
   - Vercel reads `vercel.json` automatically
   - Uses `requirements-vercel.txt` (minimal dependencies)
   - **Note**: This version has limited emotion detection accuracy

4. **Access**:
   - Vercel provides: `https://your-app.vercel.app`

### Limitations:
- ❌ No librosa (no proper audio feature extraction)
- ❌ No TensorFlow (no ML model)
- ❌ Basic amplitude-based heuristics only
- ✅ Fast deployment
- ✅ Free tier available

**Use Vercel only for testing the UI, not for production emotion recognition.**

---

## 🐳 Option 5: Docker (Any Platform)

Universal deployment using Docker.

### Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run:

```bash
# Build
docker build -t speech-emotion-recognition .

# Run locally
docker run -p 8000:8000 speech-emotion-recognition

# Deploy to any Docker platform
# - AWS ECS
# - Azure Container Apps
# - DigitalOcean App Platform
# - Fly.io
```

---

## 📊 Platform Comparison

| Platform | Ease | Cost | ML Support | Recommended |
|----------|------|------|------------|-------------|
| **Railway** | ⭐⭐⭐⭐⭐ | $5/mo | ✅ Full | ✅ **Best** |
| **Render** | ⭐⭐⭐⭐⭐ | $7/mo | ✅ Full | ✅ **Best** |
| **Cloud Run** | ⭐⭐⭐ | Pay-per-use | ✅ Full | ✅ Production |
| **Vercel** | ⭐⭐⭐⭐⭐ | Free | ❌ Limited | ⚠️ UI only |
| **Fly.io** | ⭐⭐⭐⭐ | $3/mo | ✅ Full | ✅ Good |

---

## 🚀 Quick Deploy Commands

### Railway:
```bash
railway login
railway init
railway up
```

### Render:
```bash
# Push to GitHub, then connect via Render dashboard
git push origin main
```

### Vercel (limited):
```bash
vercel --prod
```

### Cloud Run:
```bash
gcloud run deploy speech-emotion-recognition --source .
```

---

## 🔧 Environment Variables

No environment variables are required for basic deployment. Optional:

- `PORT` - Server port (auto-set by platforms)
- `PYTHON_VERSION` - Python version (3.11 recommended)

---

## ✅ Post-Deployment Checklist

After deploying:

1. ✅ Test microphone recording
2. ✅ Check `/health` endpoint
3. ✅ Test emotion prediction with sample audio
4. ✅ Verify API docs at `/docs`
5. ✅ Check response times (should be < 3s)

---

## 🆘 Troubleshooting

### "Module not found" errors:
```bash
# Ensure all dependencies in requirements.txt
pip freeze > requirements.txt
```

### Audio processing errors:
```bash
# Install system audio libraries
apt-get install libsndfile1 ffmpeg
```

### Out of memory:
- Increase memory allocation (Railway: 2GB+, Render: Starter plan)
- Use lighter model

### Slow cold starts:
- Use Railway or Render (always-on plans)
- Implement health check pinging

---

## 🎯 Recommended Deployment Path

**For Most Users:**
1. Deploy to **Railway** (easiest, full features)
2. Get public URL
3. Test thoroughly
4. Scale as needed

**For Production:**
1. Use **Google Cloud Run** or **Render**
2. Set up custom domain
3. Add monitoring
4. Implement caching

**For Quick Demo:**
1. Use **Vercel** (limited ML)
2. Show UI/UX
3. Upgrade to Railway for full features

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Vercel Docs](https://vercel.com/docs)

Happy deploying! 🚀
