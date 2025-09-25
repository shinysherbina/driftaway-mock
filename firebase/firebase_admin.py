import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_trip_context(uid: str) -> dict | None:
    """
    Returns a mock trip context for the given UID.
    In a real application, this would fetch data from a database.
    """
    logging.info(f"Fetching mock trip context for uid: {uid}")

    # Mock trip data
    mock_trip = {
        "destination": "Paris, France",
        "startDate": "2025-10-15",
        "endDate": "2025-10-22",
        "tripStyle": ["sightseeing", "foodie", "romantic"],
        "travelers": ["couple"],
    }

    return mock_trip