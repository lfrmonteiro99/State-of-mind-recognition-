# Render Deployment - 5 Minute Quick Start

Ultra-simple version for those who want to deploy NOW.

## ✅ Step-by-Step Checklist

### 1️⃣ Push to GitHub (1 min)
```bash
git push origin claude/speech-emotion-recognition-2maeP
```
✅ Done? Move to step 2

### 2️⃣ Sign Up for Render (1 min)
1. Go to **[render.com](https://render.com)**
2. Click **"Get Started"**
3. Sign up with GitHub (easiest)

✅ Done? Move to step 3

### 3️⃣ Create Web Service (1 min)
1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Find your repo: **"State-of-mind-recognition-"**
4. Click **"Connect"**

✅ Done? Move to step 4

### 4️⃣ Fill the Form (2 mins)

**Only fill these fields:**

```
Name: speech-emotion-recognition
Branch: claude/speech-emotion-recognition-2maeP
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type: Starter ($7/month)
```

**Click "Advanced"** and add:
```
Health Check Path: /health
```

**That's it!** Leave everything else as default.

✅ Done? Move to step 5

### 5️⃣ Deploy! (Click Button)
Click **"Create Web Service"** at the bottom

⏳ **Wait 10-15 minutes** for first build

✅ When you see "Your service is live", you're done!

---

## 🎉 Your App is Live!

**URL:** `https://speech-emotion-recognition.onrender.com`

**Test it:**
1. Open the URL
2. Click "Start Recording"
3. Speak for 3 seconds
4. Click "Stop & Analyze"
5. See your emotion! 🎤

---

## 💰 Cost

**Starter Plan: $7/month**
- Need this for ML libraries (2GB RAM required)
- Free tier only has 512MB (won't work)

**Want free trial?** Some regions get $50 credit = ~7 months free!

---

## 🔧 Common Issues

**"Out of memory" error?**
→ Must use Starter plan (not Free)

**App won't start?**
→ Check Start Command has `--port $PORT`

**Can't find repo?**
→ Click "Configure account" and authorize Render

---

## 📝 Need More Details?

See **[RENDER_SETUP.md](RENDER_SETUP.md)** for:
- Field-by-field explanation
- Screenshots guide
- Troubleshooting
- Monitoring tips
- Custom domain setup

---

## 🚀 That's It!

Total time: **5 minutes setup + 10 minutes build = 15 minutes to live app**

Easier than you thought, right? 😄
