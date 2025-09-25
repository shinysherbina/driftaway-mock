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
async def get_primary_transport(data: TripRequest):
    """
    Provides mock primary transport options.
    """
    logger.info(f"Received request for mock primary transport options for UID: {data.uid}")

    mock_transport = {
        "transport_options": [
            {"type": "Airplane", "details": "Flights are available from major airports to Charles de Gaulle Airport (CDG)."},
            {"type": "Train", "details": "High-speed trains (TGV) connect Paris to other major European cities."}
        ]
    }

    return mock_transport
