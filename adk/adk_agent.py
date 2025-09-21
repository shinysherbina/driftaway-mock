import os
import logging
import json
from dotenv import load_dotenv
import google.generativeai as genai
from firebase_utils import get_trip_context

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# Define the fields we care about
VALID_FIELDS = ["weather", "hotel", "food", "activities", "primaryTransport", "budget", "localTransport"]

def _sanitize_for_json(data):
    def convert(obj):
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return obj
    return convert(data)

def chat(uid: str, destination: str, message: str, session_history: list) -> dict:
    """
    Generates a calm, friendly response to the user's message.
    Nudges them toward filling in missing preferences.
    """
    trip_context = get_trip_context(uid)
    if not trip_context:
        return {
            "session_history": session_history + [
                {
                    "role": "assistant",
                    "content": "Hmm, I couldn't find your trip details. Could you try again?"
                }
            ]
        }


    prompt = f"""
    You're a warm, friendly travel assistant helping someone plan a trip to {destination}.
    They've just sent you a message, and you want to respond in a relaxed, conversational tone.

    Use their trip context to understand what they've already shared, and gently guide them toward filling in anything that's still missing—like hotel preferences, food choices, activities, transport, or budget.

    Don't overwhelm them with questions. Instead, respond like a thoughtful companion who’s genuinely curious and excited to help.

    User message: "{message}"

    Trip context:
    {json.dumps(_sanitize_for_json(trip_context), indent=2)}

    Respond with a single friendly paragraph. Avoid lists, markdown, or structured formatting—just natural language.

    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return {
            "session_history": session_history + [
            { "role": "user", "content": message },
            { "role": "assistant", "content": response.text.strip() }
            ]
        }


    except Exception as e:
        logger.error(f"Gemini chat generation failed: {e}")
        return {
            "session_history": session_history + [
                { "role": "user", "content": message },
                {
                    "role": "assistant",
                    "content": "Oops, something went wrong while generating a reply. Let's try again in a moment."
                }
            ]
        }
