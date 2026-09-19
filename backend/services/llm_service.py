"""
Groq LLM integration for personalized business advice.
Graceful fallback: if Groq not configured, returns None.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None

from config import GROQ_MAX_TOKENS, GROQ_MODEL, GROQ_TEMPERATURE


_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    if Groq is None:
        return None
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or "xxxxx" in api_key.lower() or api_key.startswith("gsk_your"):
        return None
    try:
        _client = Groq(api_key=api_key)
        return _client
    except Exception as e:
        print(f"[llm_service] Groq client init failed: {e}")
        return None


def is_llm_available() -> bool:
    return _get_client() is not None


def _lang_name(code: str) -> str:
    return {"hi": "Hindi", "en": "English", "mr": "Marathi"}.get(code, "English")


def generate_advice(
    village: str,
    taluka: str,
    district: str,
    population: Optional[int],
    crops: str,
    region: str,
    capital: int,
    category: str,
    experience: str,
    businesses: List[Dict],
    language: str = "en",
) -> Optional[Dict]:
    client = _get_client()
    if client is None:
        return None

    lang_name = _lang_name(language)
    biz_lines = "\n".join([
        f"- {b.get('n', b.get('name', 'Business'))}: "
        f"cost Rs.{b.get('cost', 0)}, monthly revenue Rs.{b.get('rev', 0)}, "
        f"monthly profit Rs.{b.get('profit', 0)}, ROI {b.get('roi', 0)}%"
        for b in businesses[:4]
    ])

    system_prompt = (
         "You are an experienced rural business advisor for Maharashtra, India. "
        "You give practical, evidence-based, culturally-appropriate advice to "
        "small rural entrepreneurs. "
        f"You MUST respond in {lang_name} language ONLY. "
        "Every string value in your JSON response must be in that language. "
        "You always respond with valid JSON only."
    )

    user_prompt = f"""Village profile:
- Village: {village}
- Taluka: {taluka}
- District: {district}
- Population: {population if population else 'unknown'}
- Main crops: {crops}
- Region: {region}

User profile:
- Available capital: Rs.{capital}
- Interested category: {category}
- Experience: {experience} years

Top recommended businesses:
{biz_lines}

TASK: Generate personalized advice in {lang_name} language.
Respond with ONLY this JSON structure (no extra text):

{{
  "business_reasons": {{
    "<exact business name 1>": "<2-3 line personalized reason>",
    "<exact business name 2>": "<2-3 line personalized reason>",
    "<exact business name 3>": "<2-3 line personalized reason>",
    "<exact business name 4>": "<2-3 line personalized reason>"
  }},
  "hyperlocal_summary": "<3-4 line natural analysis mentioning village, taluka, crops>",
  "custom_action_plan": [
    "<step 1 personalized to user's capital>",
    "<step 2>",
    "<step 3>",
    "<step 4>",
    "<step 5>"
  ],
  "executive_summary": "<4-line summary for bank officer>"
}}

IMPORTANT:
- Use exact business names as given
- All values in {lang_name}
- Mention actual Rs. amounts and village names
- ONLY return JSON, no other text
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        for key in ("business_reasons", "hyperlocal_summary",
                    "custom_action_plan", "executive_summary"):
            if key not in data:
                print(f"[llm_service] missing key: {key}")
                return None
        return data
    except Exception as e:
        print(f"[llm_service] Groq call failed: {e}")
        return None