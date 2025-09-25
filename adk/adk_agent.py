import logging

# Configure logging
logger = logging.getLogger(__name__)

def get_trip_context(uid: str) -> dict | None:
    """
    Returns a mock trip context for the given UID.
    """
    logging.info(f"Fetching mock trip context for uid: {uid}")
    return {
        "destination": "Paris, France",
        "startDate": "2025-10-15",
        "endDate": "2025-10-22",
        "tripStyle": ["sightseeing", "foodie", "romantic"],
        "travelers": ["couple"],
    }

def chat(uid: str, destination: str, message: str, session_history: list) -> dict:
    """
    Generates a mock, friendly response to the user's message.
    """
    logger.info(f"Generating mock chat response for UID: {uid}")

    mock_response = {
        "session_history": session_history + [
            {"role": "user", "content": message},
            {
                "role": "assistant",
                "content": "That sounds like a wonderful plan! I've made a note of it. What other details should we consider for your trip to Paris? Perhaps we can think about some budget options?"
            }
        ]
    }

    return mock_response
