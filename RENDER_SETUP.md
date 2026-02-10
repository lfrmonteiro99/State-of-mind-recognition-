# Render Deployment Guide - Step by Step

Complete guide to deploy your Speech Emotion Recognition app on Render.

## Part 1: Push Code to GitHub (If Not Done Already)

```bash
# Ensure all changes are committed
git status
git add .
git commit -m "Ready for Render deployment"
git push origin claude/speech-emotion-recognition-2maeP
```

## Part 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (recommended) or email

## Part 3: Connect GitHub Repository

1. After logging in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** next to GitHub
4. Authorize Render to access your GitHub
5. In the repository list, find **"State-of-mind-recognition-"**
6. Click **"Connect"**

**Note:** If you don't see your repo, click "Configure account" and give Render access to it.

## Part 4: Configure Web Service

Now you'll see a form with many fields. Fill them exactly as shown below:

### Basic Settings

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `speech-emotion-recognition` | Can be anything, this becomes your URL |
| **Region** | `Oregon (US West)` | Or choose closest to you |
| **Branch** | `claude/speech-emotion-recognition-2maeP` | Your development branch |
| **Root Directory** | Leave empty | App is in root directory |
| **Runtime** | `Python 3` | Auto-detected |

### Build & Deploy Settings

| Field | Value | Notes |
|-------|-------|-------|
| **Build Command** | `pip install -r requirements.txt` | Default is correct |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` | Important! |

**CRITICAL:** The start command MUST include `--port $PORT` (Render provides this variable)

### Advanced Settings (Click "Advanced" to expand)

| Field | Value | Notes |
|-------|-------|-------|
| **Auto-Deploy** | `Yes` | ✅ Enable (deploys on git push) |
| **Health Check Path** | `/health` | Optional but recommended |

### Environment Variables

Click **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Recommended version |
| `PORT` | (leave empty) | Render sets this automatically |

**Note:** You don't need to add PORT manually - Render provides it automatically.

## Part 5: Choose Instance Type

| Field | Value | Cost | Notes |
|-------|-------|------|-------|
| **Instance Type** | `Starter` | **$7/month** | Required for ML libraries |

**Why not Free?**
- Free tier has only 512MB RAM
- TensorFlow + Librosa need ~2GB RAM
- Free tier sleeps after 15 min inactivity
- **Starter gives 2GB RAM + always-on**

**Free Tier Alternative:**
If you want to try free first:
1. Select "Free"
2. It might work but could crash due to memory limits
3. Upgrade to Starter if you get memory errors

## Part 6: Create Web Service

1. Review all settings
2. Click **"Create Web Service"** (bottom)
3. Render starts building your app

## Part 7: Wait for Deployment

You'll see the build logs in real-time:

```
==> Downloading Python dependencies
==> Installing packages from requirements.txt
==> Building...
==> Downloading librosa...
==> Installing tensorflow...
==> Build completed successfully
==> Deploying...
==> Your service is live at https://speech-emotion-recognition.onrender.com
```

**First deployment takes 8-15 minutes** (installing TensorFlow + ML libraries)

### Common Build Messages (Don't Worry About These):
- `WARNING: Running pip as root` - Normal on Render
- `Building wheels for scipy` - Takes time, be patient
- `Collecting tensorflow` - Large download, wait for it

## Part 8: Get Your URL

After deployment succeeds:

1. Look for **"Your service is live at..."**
2. Your URL will be: `https://speech-emotion-recognition.onrender.com`
3. Click the URL or copy it

**Note:** Replace `speech-emotion-recognition` with whatever name you chose in step 4.

## Part 9: Test Your Deployment

1. Open your Render URL in browser
2. Click "Start Recording"
3. Allow microphone access
4. Speak for 3-5 seconds
5. Click "Stop & Analyze"
6. See emotion predictions!

## Part 10: Configure Custom Domain (Optional)

If you own a domain:

1. Go to your Web Service dashboard
2. Click "Settings" tab
3. Scroll to "Custom Domain"
4. Click "Add Custom Domain"
5. Enter your domain: `emotions.yourdomain.com`
6. Follow DNS instructions (add CNAME record)

## Quick Reference: Complete Field Values

**Copy-paste these values:**

```
Name: speech-emotion-recognition
Region: Oregon (US West)
Branch: claude/speech-emotion-recognition-2maeP
Root Directory: (empty)
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type: Starter ($7/month)
Auto-Deploy: Yes
Health Check Path: /health
```

**Environment Variables:**
```
PYTHON_VERSION=3.11.0
```

## Troubleshooting

### Build Fails with "Out of Memory"
**Solution:** Upgrade to Starter plan (need 2GB+ RAM)

### "No module named 'librosa'" Error
**Solution:**
- Check Build Command is: `pip install -r requirements.txt`
- Ensure `requirements.txt` is in repository root

### Service Won't Start / Health Check Failing
**Solution:**
- Check Start Command includes `--port $PORT`
- Verify Health Check Path is `/health` (not `/api/health`)

### Audio Processing Errors
**Solution:**
- FFmpeg is auto-installed on Render
- If errors persist, contact Render support

### App is Slow on First Request
**Reason:** This is normal! ML model loads on first request
**Solution:**
- Upgrade to Starter (keeps instance warm)
- Or accept 5-10s delay on first request

## Monitoring Your Deployment

### View Logs
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time server logs

### Check Metrics
1. Click "Metrics" tab
2. See CPU, Memory, Request count
3. Monitor for issues

### View Events
1. Click "Events" tab
2. See deployment history
3. Track successes/failures

## Updating Your Deployment

### Automatic (Recommended)
1. Make changes locally
2. Commit and push:
```bash
git add .
git commit -m "Update feature"
git push origin claude/speech-emotion-recognition-2maeP
```
3. Render auto-deploys in 2-5 minutes

### Manual
1. Go to service dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"

## Cost Breakdown

| Plan | RAM | CPU | Cost | Best For |
|------|-----|-----|------|----------|
| **Free** | 512MB | Shared | $0 | Testing only |
| **Starter** | 2GB | Shared | $7/mo | This app ✅ |
| **Standard** | 4GB | 1 CPU | $25/mo | Heavy traffic |
| **Pro** | 8GB | 2 CPU | $85/mo | Production |

**Recommendation:** Start with **Starter ($7/mo)**

## Free Credits

Render offers:
- **$50 free credit** for new accounts (some regions)
- Check their promotions page
- Covers ~7 months of Starter plan!

## Alternative: Free Tier Setup (Limited)

If you want to try free tier despite limitations:

1. Choose "Free" instance type
2. App will sleep after 15 min inactivity
3. First request after sleep: 30-60s delay
4. May crash with memory errors
5. Good for testing, not for real use

**To reduce memory:**
- Remove `tensorflow` from requirements.txt
- App uses simpler heuristic model
- Less accurate but fits in 512MB

## Summary

**Minimum Steps:**
1. Push code to GitHub ✅
2. Create Render account ✅
3. Connect GitHub repo ✅
4. Fill form with values above ✅
5. Choose Starter plan ✅
6. Click "Create Web Service" ✅
7. Wait 10 minutes ✅
8. Use your app! ✅

**Your app will be live at:**
`https://speech-emotion-recognition.onrender.com`

**Need help?** Check Render docs or their Discord community!

---

**Next Steps After Deployment:**
- Share your URL with friends
- Test on mobile devices
- Monitor usage in dashboard
- Consider custom domain
- Train your own emotion model

Good luck! 🚀
