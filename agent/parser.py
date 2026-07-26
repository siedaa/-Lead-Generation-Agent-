import json
import re
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def parse_prompt(user_text: str) -> dict:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract a business category and a location from the user's "
                        "sentence. Respond with ONLY a JSON object like "
                        '{"category": "...", "location": "..."} and nothing else — '
                        "no markdown, no explanation, no additional text."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
        )
        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)
        category = str(data.get("category", "")).strip()
        location = str(data.get("location", "")).strip()
        return {"category": category, "location": location}
    except Exception:
        match = re.split(r"\s+in\s+", user_text, flags=re.IGNORECASE)
        if len(match) == 2:
            return {"category": match[0].strip(), "location": match[1].strip()}
        return {"category": user_text.strip(), "location": ""}