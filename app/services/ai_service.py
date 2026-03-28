import requests
from app.core.config import settings


def analyze_and_match(description, ngos, volunteers):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={settings.GEMINI_API_KEY}"

        prompt = f"""
You are an intelligent AI for NGO and volunteer matching.

-------------------------
CATEGORIES:
- food → hunger, starving
- medical → injury, illness
- shelter → homeless
- elderly → old people needing care
- other → anything else

URGENCY:
- high → life-threatening (hunger, injury)
- medium → needs help
- low → minor issue

-------------------------
INPUT:

Problem:
{description}

NGOs (JSON):
{ngos}

Volunteers (JSON):
{volunteers}

-------------------------
INSTRUCTIONS:

1. Identify correct category
2. Identify urgency
3. Select NGO whose skills match category
4. Select volunteers whose skills match category

-------------------------
OUTPUT (STRICT JSON ONLY):

{{
  "category": "...",
  "urgency": "...",
  "best_ngo": "...",
  "matched_volunteers": ["..."]
}}

ONLY JSON. NO TEXT.
"""

        body = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        response = requests.post(url, json=body)
        result = response.json()

        print("AI RAW RESPONSE:", result)

        candidates = result.get("candidates", [])
        if not candidates:
            return "{}"

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return "{}"

        text = parts[0].get("text", "").strip()

        # 🔥 CLEAN RESPONSE
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()

        return text

    except Exception as e:
        print("AI ERROR:", str(e))
        return "{}"