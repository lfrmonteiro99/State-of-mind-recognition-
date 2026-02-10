# Full Analysis Feature Guide

The Full Analysis feature provides deep insights into your state of mind by combining:
1. **Speech transcription** (what you said)
2. **Emotion detection** (how you said it)
3. **AI-powered analysis** (what it means + advice)

## Features

### 🎯 What You Get

**Standard Mode (Default):**
- ⚡ Fast emotion detection
- 📊 Confidence scores
- 🎨 Visual emotion breakdown

**Full Analysis Mode:**
- ✅ Everything in Standard Mode
- 📝 Speech transcription (what you said)
- 💭 Emotional analysis (how your words relate to emotions)
- 🎯 State of mind assessment
- 💡 Personalized advice and next steps

## How to Use

### Step 1: Enable Full Analysis

1. Click the checkbox: **"Full Analysis (includes transcription + AI insights)"**
2. Start recording
3. Speak for 3-10 seconds (the longer, the better the analysis)
4. Click "Stop & Analyze"

### Step 2: View Your Results

You'll see three sections:

**1. Emotion Analysis** (always shown)
- Top detected emotion
- All emotion probabilities

**2. What You Said** (Full Analysis only)
- Transcription of your speech
- Automatically transcribed using AI

**3. State of Mind Analysis** (Full Analysis only)
- **Emotional Analysis:** How your words connect to your emotions
- **State of Mind:** Assessment of your mental/emotional state
- **Supportive Advice:** Personalized, actionable guidance

## Configuration

### AI-Powered Insights (Optional)

For the best analysis, add an OpenAI API key:

1. Get a key from: https://platform.openai.com/api-keys
2. Create a `.env` file:
```bash
cp .env.example .env
```
3. Add your key:
```
OPENAI_API_KEY=sk-your-key-here
```

**Without API key:** You'll get rule-based analysis (still helpful!)
**With API key:** Advanced AI-powered insights using GPT-3.5

### Cost

**OpenAI API (if used):**
- ~$0.002 per analysis (very cheap!)
- Monthly limit: Set in OpenAI dashboard
- Can disable anytime

**Whisper transcription:**
- Runs locally (free!)
- No API needed

## Technical Details

### How It Works

```
┌─────────────────────────────────────────┐
│ You speak into microphone               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Audio Analysis (parallel)               │
├─────────────────────────────────────────┤
│ 1. Feature extraction → Emotion         │
│ 2. Whisper → Transcription              │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ AI Analysis                             │
├─────────────────────────────────────────┤
│ GPT-3.5 analyzes:                       │
│ - What you said (text)                  │
│ - How you said it (emotion)             │
│ - Context clues                         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Results                                 │
├─────────────────────────────────────────┤
│ - Emotional analysis                    │
│ - State of mind assessment              │
│ - Personalized advice                   │
└─────────────────────────────────────────┘
```

### Performance

**Standard Mode:**
- Response time: ~1-2 seconds
- No external API calls

**Full Analysis Mode:**
- Transcription: +2-3 seconds (local Whisper)
- AI analysis: +1-2 seconds (OpenAI API)
- Total: ~4-7 seconds

**Why the difference?**
- Whisper model loads first time (one-time cost)
- Transcription processes entire audio
- AI generates thoughtful responses

## Privacy & Security

### What Gets Sent

**Standard Mode:**
- ✅ Audio stays on server
- ✅ Processed locally
- ❌ Nothing sent to external services

**Full Analysis Mode:**
- ✅ Audio processed locally (Whisper)
- ⚠️ Transcription + emotion sent to OpenAI (if API key configured)
- ❌ Audio itself never sent to OpenAI

### Data Retention

- Audio: Not stored (processed in memory)
- Transcriptions: Not stored
- Analysis: Not stored
- OpenAI: May store prompts per their policy

**To maximize privacy:**
- Don't provide OpenAI API key
- Uses local rule-based analysis instead
- 100% private, zero external calls

## Use Cases

### Personal Development
- Track emotional patterns
- Understand thought-emotion connections
- Get actionable self-improvement advice

### Mental Health Support
- Express feelings and get supportive feedback
- Identify emotional states you may not recognize
- Receive gentle guidance on next steps

**Note:** This is not a replacement for professional mental health care!

### Communication Practice
- Analyze how you express yourself
- Understand emotional tone
- Practice clearer communication

### Journaling
- Speak your thoughts instead of writing
- Get AI-powered reflection
- Track emotional journey over time

## Examples

### Example 1: Happy State

**You say:**
> "I just got promoted at work! I can't believe it happened. I've been working so hard for this."

**Emotion detected:** Happy (85% confidence)

**Analysis:**
- **Emotional Analysis:** Your excitement and disbelief show genuine joy mixed with surprise. This achievement feels earned but unexpected.
- **State of Mind:** You're experiencing positive emotions tied to validation and recognition. Your mental state is elevated and optimistic.
- **Advice:** Celebrate this moment! Share it with loved ones. Reflect on what led to this success so you can repeat it. Use this positive energy to set new goals.

### Example 2: Stressed State

**You say:**
> "I have so much to do and not enough time. Everything is piling up and I don't know where to start."

**Emotion detected:** Fear (65% confidence) + Sad (20%)

**Analysis:**
- **Emotional Analysis:** Your words reveal overwhelm and anxiety. You're feeling paralyzed by too many demands simultaneously.
- **State of Mind:** You're in a stressed state, experiencing decision fatigue. Your mind is scanning for control but finding chaos.
- **Advice:** Pause and take three deep breaths. Write down all tasks, then pick just ONE to start with - preferably the smallest. Breaking the paralysis is more important than choosing the "right" task. Consider asking for help.

### Example 3: Neutral/Reflective

**You say:**
> "I'm thinking about making some changes in my life. Not sure what yet, but something needs to shift."

**Emotion detected:** Neutral (60% confidence)

**Analysis:**
- **Emotional Analysis:** Your calm tone suggests thoughtful contemplation rather than crisis. You're in an exploratory mindset.
- **State of Mind:** You're in a balanced but transitional state, open to change without urgency. This is a good mental space for planning.
- **Advice:** Use this clarity to explore what specifically feels off. Journal or talk to someone about what "shift" means to you. No need to rush - this reflective state is valuable for making wise decisions.

## Troubleshooting

### "Transcription unavailable"

**Cause:** Whisper model failed to load
**Solution:**
```bash
# Reinstall whisper
pip uninstall openai-whisper
pip install openai-whisper==20231117
```

### "Analysis error"

**Cause:** OpenAI API issue
**Solution:**
- Check API key in `.env`
- Verify key is active: https://platform.openai.com/api-keys
- Check you have credits
- Falls back to rule-based analysis automatically

### Slow transcription

**Cause:** Using large Whisper model
**Solution:** Model size is set to "base" (good balance). For faster:
- Edit `backend/speech_transcriber.py`
- Change `model_size="base"` to `"tiny"`
- Trade-off: less accurate transcription

### High memory usage

**Cause:** Whisper model loaded in memory
**Solution:** Normal behavior. Model is ~140MB. Unloads after inactivity.

## FAQ

**Q: Do I need an OpenAI API key?**
A: No! Without it, you get rule-based analysis. With it, you get AI-powered insights.

**Q: Is my data private?**
A: Audio is processed locally. Only text+emotion sent to OpenAI if you provide API key.

**Q: How accurate is the transcription?**
A: Very good for clear speech. Whisper is state-of-the-art. Accuracy ~95%+ for English.

**Q: Can it detect sarcasm?**
A: Partially. Emotion detection might catch tonal cues. AI analysis helps interpret context.

**Q: What languages are supported?**
A: Currently optimized for English. Whisper supports 90+ languages but analysis prompt is English.

**Q: Can I use this for therapy?**
A: This is a supportive tool, NOT a replacement for professional mental health care.

**Q: Will this work offline?**
A: Partially. Transcription works offline. AI analysis needs internet (unless you remove API key).

## Advanced: Customizing Analysis

Want to customize the AI analysis? Edit `backend/mind_analyzer.py`:

```python
# Change the system prompt (line 30)
"You are an empathetic mental health assistant..."

# Modify to your preference:
"You are a supportive life coach..."
"You are a mindfulness guide..."
"You are a communication expert..."
```

Change temperature for creativity (line 43):
```python
temperature=0.7  # Default (balanced)
temperature=0.3  # More consistent
temperature=1.0  # More creative/varied
```

## Support

**Issues?** Open an issue on GitHub with:
- What you said (if comfortable sharing)
- Detected emotion
- Error message (if any)

**Feature requests?** Let us know what kind of analysis would help you most!

---

**Remember:** This tool is designed to support self-awareness and growth. Be kind to yourself! 💚
