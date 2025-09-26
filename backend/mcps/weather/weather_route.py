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
async def get_weather(data: TripRequest):
    """
    Provides mock weather forecast.
    """
    logger.info(f"Received request for mock weather forecast for UID: {data.uid}")

    mock_weather = {
        "forecast": [
            {"day": 1, "summary": "Sunny", "temperature": "22°C"},
            {"day": 2, "summary": "Partly cloudy", "temperature": "20°C"},
            {"day": 3, "summary": "Light rain", "temperature": "18°C"}
        ]
    }

    return mock_weather
