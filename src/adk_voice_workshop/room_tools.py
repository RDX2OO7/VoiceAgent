from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def search_hotels(location: str, max_price: str = "", preferences: str = "") -> dict:
    """Search for actual real hotels in any designated location using live web search.

    Args:
        location: City, neighborhood, landmark, or region where the user wants to find hotels (e.g. 'Mumbai', 'Paris', 'New York', 'Goa').
        max_price: Optional budget or maximum price range (e.g. '$150 per night', 'under 5000 INR').
        preferences: Optional preferences (e.g. 'near beach', '5-star luxury', 'free breakfast', 'pool').
    """
    if not location or not location.strip():
        return {"status": "error", "message": "Please specify a location to search for hotels."}

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Neither GEMINI_API_KEY nor GOOGLE_API_KEY is configured in .env")
        return {
            "status": "error",
            "message": "API key is missing in environment configuration.",
        }

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        prompt = (
            f"Find 3 to 4 actual, real, open hotels in or near '{location.strip()}'.\n"
            f"User preferences: '{preferences}'. Price limit/budget: '{max_price}'.\n"
            "Provide accurate ratings, estimated price ranges, exact addresses/neighborhoods, and highlights.\n"
            "Return a clean JSON object with key 'hotels' containing an array of objects with keys: "
            "'name', 'rating', 'price_range', 'location', 'highlights'."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2,
            ),
        )

        text_output = response.text or ""

        if "```json" in text_output:
            json_str = text_output.split("```json")[1].split("```")[0].strip()
            data = json.loads(json_str)
            if isinstance(data, dict) and "hotels" in data:
                return {"status": "success", "location": location, "hotels": data["hotels"]}
            elif isinstance(data, list):
                return {"status": "success", "location": location, "hotels": data}
        elif text_output.strip().startswith("{") and "hotels" in text_output:
            try:
                data = json.loads(text_output.strip())
                return {"status": "success", "location": location, "hotels": data.get("hotels", [])}
            except Exception:
                pass

        return {
            "status": "success",
            "location": location,
            "summary": text_output.strip(),
        }

    except Exception as exc:
        logger.exception("Error during hotel search for location %s", location)
        return {
            "status": "error",
            "message": f"Could not retrieve hotels for {location}: {str(exc)}",
        }


def find_rooms(location: str = "Mumbai", minimum_capacity: int = 1) -> dict:
    """Legacy compatibility wrapper that searches for hotels/rooms in a location."""
    return search_hotels(location=location)
