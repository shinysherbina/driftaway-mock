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

@router.post("/", tags=["Transport"])
async def get_local_transport(data: TripRequest):
    """
    Provides mock local transport options.
    """
    logger.info(f"Received request for mock local transport options for UID: {data.uid}")

    mock_transport = {
        "transport_options": [
            {"type": "Metro", "details": "The Paris Métro is a convenient and efficient way to get around the city."},
            {"type": "Bus", "details": "Buses offer a scenic way to travel and cover areas not served by the metro."},
            {"type": "Vélib'", "details": "A public bicycle sharing system available throughout Paris."}
        ]
    }

    return mock_transport
