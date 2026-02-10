import openai
import os
from typing import Dict, Optional


class MindAnalyzer:
    """
    Analyzes speech content combined with detected emotions to provide
    insights and advice about mental state.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the analyzer.

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key

    def analyze_state_of_mind(
        self,
        transcription: str,
        emotion: str,
        confidence: float,
        all_emotions: Dict[str, float]
    ) -> Dict[str, str]:
        """
        Analyze the speaker's state of mind based on what they said and how they said it.

        Args:
            transcription: What the person said (text)
            emotion: Top detected emotion
            confidence: Confidence score for top emotion
            all_emotions: All emotion probabilities

        Returns:
            Dictionary with analysis and advice
        """
        if not self.api_key:
            return self._fallback_analysis(transcription, emotion, confidence)

        try:
            # Create analysis prompt
            prompt = self._build_analysis_prompt(
                transcription, emotion, confidence, all_emotions
            )

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an empathetic mental health assistant. "
                            "Analyze speech content and emotion to provide supportive insights. "
                            "Be compassionate, non-judgmental, and helpful. "
                            "Keep responses concise (3-4 sentences per section)."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )

            analysis_text = response.choices[0].message.content.strip()

            # Parse response into sections
            return self._parse_analysis(analysis_text)

        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self._fallback_analysis(transcription, emotion, confidence)

    def _build_analysis_prompt(
        self,
        transcription: str,
        emotion: str,
        confidence: float,
        all_emotions: Dict[str, float]
    ) -> str:
        """Build the analysis prompt for the LLM."""
        # Get secondary emotions (top 3)
        sorted_emotions = sorted(
            all_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        secondary_emotions = ", ".join(
            [f"{e[0]} ({e[1]*100:.0f}%)" for e in sorted_emotions[1:]]
        )

        prompt = f"""
Analyze this person's state of mind based on their speech:

**What they said:**
"{transcription}"

**How they said it (emotions detected):**
- Primary emotion: {emotion} ({confidence*100:.0f}% confidence)
- Secondary emotions: {secondary_emotions}

Please provide:

1. **Emotional Analysis**: How does what they said relate to their emotional state? What might be underlying their words?

2. **State of Mind**: What does this tell us about their current mental/emotional state?

3. **Supportive Advice**: What constructive advice or next steps would help them? Be specific and actionable.

Format your response as:
**Emotional Analysis:**
[your analysis]

**State of Mind:**
[your assessment]

**Advice:**
[your advice]
"""
        return prompt

    def _parse_analysis(self, analysis_text: str) -> Dict[str, str]:
        """Parse the LLM response into structured sections."""
        sections = {
            "emotional_analysis": "",
            "state_of_mind": "",
            "advice": ""
        }

        # Try to extract sections
        lines = analysis_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()

            if "emotional analysis" in line.lower():
                current_section = "emotional_analysis"
            elif "state of mind" in line.lower():
                current_section = "state_of_mind"
            elif "advice" in line.lower():
                current_section = "advice"
            elif line and current_section and not line.startswith('**'):
                sections[current_section] += line + " "

        # Clean up
        for key in sections:
            sections[key] = sections[key].strip()

        # If parsing failed, put everything in emotional_analysis
        if not any(sections.values()):
            sections["emotional_analysis"] = analysis_text

        return sections

    def _fallback_analysis(
        self,
        transcription: str,
        emotion: str,
        confidence: float
    ) -> Dict[str, str]:
        """
        Provide basic rule-based analysis when AI is not available.
        """
        emotion_insights = {
            "happy": {
                "analysis": "Your positive tone suggests you're experiencing joy or satisfaction. Your words reflect an optimistic outlook.",
                "state": "You appear to be in a good mental space, feeling upbeat and positive about things.",
                "advice": "Enjoy this positive moment! Consider what led to this feeling so you can recreate it. Share your positivity with others."
            },
            "sad": {
                "analysis": "Your tone indicates you may be feeling down or discouraged. The content of your speech suggests some underlying sadness.",
                "state": "You seem to be going through a difficult time emotionally. It's okay to feel sad sometimes.",
                "advice": "Acknowledge your feelings without judgment. Reach out to someone you trust. Consider what small step might help you feel a bit better."
            },
            "angry": {
                "analysis": "Your speech shows signs of frustration or anger. There seems to be something bothering you significantly.",
                "state": "You're experiencing strong negative emotions, possibly feeling frustrated or upset about a situation.",
                "advice": "Take some deep breaths to calm down. Identify what's triggering these feelings. Consider constructive ways to address the situation once you're calmer."
            },
            "fear": {
                "analysis": "Your tone suggests anxiety or worry. You may be feeling uncertain or concerned about something.",
                "state": "You appear to be experiencing anxiety or apprehension about a situation or outcome.",
                "advice": "Focus on what you can control. Break down big worries into smaller, manageable parts. Talk to someone about your concerns."
            },
            "neutral": {
                "analysis": "Your tone is balanced and calm. You're expressing yourself in a measured way.",
                "state": "You seem to be in a stable, calm mental state without strong emotional fluctuations.",
                "advice": "This balanced state is good for clear thinking. Use this clarity to reflect on your goals or make important decisions."
            },
            "surprise": {
                "analysis": "Your speech shows unexpected reactions. You seem to be processing new or unexpected information.",
                "state": "You're experiencing surprise or astonishment, which can be either positive or negative.",
                "advice": "Take time to process this new information. Don't rush to react. Consider how this changes your perspective."
            },
            "disgust": {
                "analysis": "Your tone suggests strong aversion or disapproval about something.",
                "state": "You're feeling repelled or strongly opposed to something you've encountered.",
                "advice": "Identify what specifically bothers you. Set boundaries if needed. Focus on what aligns with your values instead."
            }
        }

        insight = emotion_insights.get(emotion, emotion_insights["neutral"])

        return {
            "emotional_analysis": insight["analysis"],
            "state_of_mind": insight["state"],
            "advice": insight["advice"]
        }
