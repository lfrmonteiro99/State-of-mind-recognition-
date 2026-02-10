# Render Form Fields - Quick Reference Card

Print or save this page. Fill the Render form exactly as shown below.

---

## 📋 Copy-Paste Values

### Basic Info
```
Name: speech-emotion-recognition
```

### Source Code
```
Branch: claude/speech-emotion-recognition-2maeP
Root Directory: (leave empty)
```

### Build Settings
```
Build Command: pip install -r requirements.txt
```

### Deploy Settings
```
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Instance
```
Instance Type: Starter
```

### Advanced Settings
```
Health Check Path: /health
Auto-Deploy: Yes
```

### Environment Variables
```
PYTHON_VERSION = 3.11.0
```

---

## ⚠️ Critical Fields

| Field | Value | Why Important |
|-------|-------|---------------|
| **Start Command** | Must include `--port $PORT` | Render needs this variable |
| **Instance Type** | Must be **Starter** | Free tier too small for ML |
| **Branch** | Your branch name | Wrong branch = wrong code |

---

## ❌ Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `--port 8000` | `--port $PORT` |
| Instance: Free | Instance: Starter |
| Branch: main | Branch: claude/speech-emotion-recognition-2maeP |
| Health: `/api/health` | Health: `/health` |

---

## 🎯 Field Locations

**If you can't find a field:**

- **Health Check Path**: Click "Advanced" button to see it
- **Auto-Deploy**: Also in "Advanced" section
- **Environment Variables**: Scroll down, look for "Add Environment Variable" button
- **Instance Type**: Middle of page, can't miss it

---

## 💡 Pro Tips

1. **Copy-paste** - Don't type these manually
2. **Double-check** the start command (`$PORT` not `8000`)
3. **Save this page** - You'll need it again for updates
4. **Ignore** other fields - defaults are fine

---

## 🚨 If Deployment Fails

Check these in order:

1. ✅ Branch name correct?
2. ✅ Start command has `$PORT`?
3. ✅ Instance type is Starter?
4. ✅ Build command matches exactly?

If all ✅ but still fails, check build logs for specific error.

---

## 📱 Screenshot Reference

Your form should look like this:

```
┌─────────────────────────────────────────┐
│ Name                                    │
│ [speech-emotion-recognition]            │
├─────────────────────────────────────────┤
│ Region                                  │
│ [Oregon (US West)         ▼]            │
├─────────────────────────────────────────┤
│ Branch                                  │
│ [claude/speech-emotion...  ▼]           │
├─────────────────────────────────────────┤
│ Build Command                           │
│ [pip install -r requirements.txt]       │
├─────────────────────────────────────────┤
│ Start Command                           │
│ [uvicorn main:app --host 0.0.0.0 ...]  │
├─────────────────────────────────────────┤
│ Instance Type                           │
│ ○ Free                                  │
│ ● Starter    $7/month                   │
│ ○ Standard   $25/month                  │
└─────────────────────────────────────────┘
     [Create Web Service]
```

---

## ⏱️ Timeline

- **Form filling**: 2-3 minutes
- **Build time**: 10-15 minutes (first time)
- **Total**: ~15 minutes to live app

---

## 🔗 Quick Links

- Full Guide: [RENDER_SETUP.md](RENDER_SETUP.md)
- Quick Start: [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md)
- Render Dashboard: [dashboard.render.com](https://dashboard.render.com)

---

**That's all you need!** Keep this page handy while filling the form.
