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
async def get_food_suggestions(data: TripRequest):
    """
    Provides mock food suggestions.
    """
    logger.info(f"Received request for mock food suggestions for UID: {data.uid}")

    mock_food = {
        "cafes": [
            {
                "name": "The Daily Grind",
                "cuisine": "Continental",
                "priceRange": "$",
                "rating": 4.2,
                "location": "City Center",
                "reason": "Great for a quick coffee and light bites.",
                "url": "https://www.mockdata.com/maps/search/The+Daily+Grind"
            },
            {
                "name": "Spice Route Cafe",
                "cuisine": "Indian",
                "priceRange": "$",
                "rating": 4.5,
                "location": "Old Town",
                "reason": "Authentic local flavors in a cozy setting.",
                "url": "https://www.mockdata.com/spice-route-cafe"
            },
            {
                "name": "Green Leaf Bistro",
                "cuisine": "Healthy",
                "priceRange": "$",
                "rating": 4.0,
                "location": "Near Park",
                "reason": "Fresh salads and organic options.",
                "url": "https://www.mockdata.com/GreenLeafBistro"
            },
            {
                "name": "Cafe Amore",
                "cuisine": "Italian",
                "priceRange": "$$",
                "rating": 4.7,
                "location": "Riverside",
                "reason": "Romantic ambiance with delicious pasta.",
                "url": "https://www.mockdata.com/maps/search/Cafe+Amore"
            }
        ]
    }

    return mock_food
