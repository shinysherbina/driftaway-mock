import logging
from fastapi import APIRouter
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TripRequest(BaseModel):
    uid: str
    destination: str

@router.post("")
async def get_activities(data: TripRequest):
    """
    Provides mock activity suggestions.
    """
    logger.info(f"Received request for mock activity suggestions for UID: {data.uid}")

    mock_activities = {
        "itinerary": [
            {
                "day": "Day 1",
                "date": "2025-09-26", # Using today's date as a placeholder
                "activities": [
                    {
                        "id": "activity_1",
                        "name": "Eiffel Tower",
                        "type": "Landmark",
                        "location": "Paris",
                        "rating": 4.8,
                        "reviewCount": 150000,
                        "imageUrl": "https://www.mockdata.com/eiffel-tower.jpg",
                        "tags": ["Iconic", "View", "Photography"],
                        "reason": "A must-see landmark with breathtaking views of Paris."
                    },
                    {
                        "id": "activity_2",
                        "name": "Louvre Museum",
                        "type": "Museum",
                        "location": "Paris",
                        "rating": 4.7,
                        "reviewCount": 120000,
                        "imageUrl": "https://www.mockdata.com/louvre-museum.jpg",
                        "tags": ["Art", "Culture", "History"],
                        "reason": "Home to thousands of works of art, including the Mona Lisa."
                    },
                    {
                        "id": "activity_3",
                        "name": "Notre Dame Cathedral",
                        "type": "Cathedral",
                        "location": "Paris",
                        "rating": 4.6,
                        "reviewCount": 90000,
                        "imageUrl": "https://www.mockdata.com/notre-dame.jpg",
                        "tags": ["Architecture", "History", "Religious"],
                        "reason": "A stunning example of French Gothic architecture."
                    },
                    {
                        "id": "activity_4",
                        "name": "Seine River Cruise",
                        "type": "Tour",
                        "location": "Paris",
                        "rating": 4.5,
                        "reviewCount": 75000,
                        "imageUrl": "https://www.mockdata.com/seine-cruise.jpg",
                        "tags": ["Relaxing", "Scenic", "Romantic"],
                        "reason": "Enjoy panoramic views of Paris landmarks from the water."
                    }
                ]
            }
        ],
        "summary": f"Your adventure itinerary for {data.destination}.",
        "location": data.destination
    }

    return mock_activities