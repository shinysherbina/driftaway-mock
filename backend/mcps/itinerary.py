import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# TODO: Implement the itinerary orchestrator that calls other MCPs to generate a full itinerary.
def generate_full_itinerary(trip_details: dict):
    """
    Generates a mock comprehensive itinerary.
    """
    destination = trip_details.get("destination", "Paris")
    user_location = trip_details.get("user_location", "London") # Assuming user_location is available in trip_details

    mock_itinerary_data = {
        "primary_transport": {
            "outbound": {
                "type": "Flight",
                "details": f"Flight from {user_location} to {destination}",
                "price": 150,
                "booking_url": "https://www.mockdata.com/flights/outbound"
            },
            "inbound": {
                "type": "Flight",
                "details": f"Flight from {destination} to {user_location}",
                "price": 120,
                "booking_url": "https://www.mockdata.com/flights/inbound"
            }
        },
        "local_transport": {
            "provider": "Zoomcar",
            "details": f"Self-drive car rental from Zoomcar for 3 days in {destination}.",
            "price": 90,
            "booking_url": "https://www.mockdata.com/zoomcar"
        },
        "daily_activities": [
            {
                "day": "Day 1",
                "date": "2025-09-26",
                "activities": [
                    {
                        "name": "Eiffel Tower Visit",
                        "type": "Landmark",
                        "time": "10:00 AM",
                        "description": "Ascend the iconic Eiffel Tower for panoramic views of Paris.",
                        "imageUrl": "https://www.mockdata.com/eiffel-tower.jpg"
                    },
                    {
                        "name": "Louvre Museum Tour",
                        "type": "Museum",
                        "time": "02:00 PM",
                        "description": "Explore world-renowned art collections, including the Mona Lisa.",
                        "imageUrl": "https://www.mockdata.com/louvre-museum.jpg"
                    }
                ]
            },
            {
                "day": "Day 2",
                "date": "2025-09-27",
                "activities": [
                    {
                        "name": "Notre Dame Cathedral",
                        "type": "Cathedral",
                        "time": "09:30 AM",
                        "description": "Admire the Gothic architecture of Notre Dame.",
                        "imageUrl": "https://www.mockdata.com/notre-dame.jpg"
                    },
                    {
                        "name": "Seine River Cruise",
                        "type": "Tour",
                        "time": "04:00 PM",
                        "description": "Enjoy a relaxing boat trip along the Seine River.",
                        "imageUrl": "https://www.mockdata.com/seine-cruise.jpg"
                    }
                ]
            }
        ],
        "cafes_to_try": [
            {
                "name": "Cafe Amore",
                "cuisine": "Italian",
                "rating": 4.7,
                "location": "Riverside",
                "reason": "Romantic ambiance with delicious pasta.",
                "url": "https://www.mockdata.com/maps/search/Cafe+Amore"
            },
            {
                "name": "The Daily Grind",
                "cuisine": "Continental",
                "rating": 4.2,
                "location": "City Center",
                "reason": "Great for a quick coffee and light bites.",
                "url": "https://www.mockdata.com/maps/search/The+Daily+Grind"
            }
        ],
        "weather_forecast": [
            {"date": "2025-09-26", "summary": "Sunny", "temperature": "22°C"},
            {"date": "2025-09-27", "summary": "Partly Cloudy", "temperature": "20°C"},
            {"date": "2025-09-28", "summary": "Light Rain", "temperature": "18°C"}
        ]
    }
    logger.info(f"Generated mock itinerary for {destination}.")
    return mock_itinerary_data

@router.get("")
async def get_full_itinerary(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides a full itinerary by orchestrating other services.
    """
    logger.info(f"Received request for full itinerary for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the placeholder orchestrator
        logger.info(f"Generating full itinerary for trip: {trip_details.get('name', 'N/A')}")
        itinerary_data = generate_full_itinerary(trip_details)

        logger.info(f"Successfully generated full itinerary for UID: {uid}")
        return itinerary_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while generating the full itinerary for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }