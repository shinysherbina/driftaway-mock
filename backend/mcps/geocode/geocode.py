import asyncio
import logging
import os
from typing import Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Geocode MCP Server 📍")

# Mock geocode data
GEOCODE_DATA = {
    "Munnar, Kerala": {
        "results": [
            {
                "formatted_address": "Munnar, Kerala, India",
                "geometry": {
                    "location": {
                        "lat": 10.0889,
                        "lng": 77.0595
                    }
                },
                "place_id": "ChIJ3S-p5Y4Z-zsR_wJ-0d-0Z8c",
            }
        ],
        "status": "OK"
    },
    "Darjeeling, West Bengal": {
        "results": [
            {
                "formatted_address": "Darjeeling, West Bengal, India",
                "geometry": {
                    "location": {
                        "lat": 27.0410,
                        "lng": 88.2663
                    }
                },
                "place_id": "ChIJz-k-0X1Z-zsR_wJ-0d-0Z8c",
            }
        ],
        "status": "OK"
    },
    "Agra, Uttar Pradesh": {
        "results": [
            {
                "formatted_address": "Agra, Uttar Pradesh, India",
                "geometry": {
                    "location": {
                        "lat": 27.1767,
                        "lng": 78.0081
                    }
                },
                "place_id": "ChIJ1-U-0X1Z-zsR_wJ-0d-0Z8c",
            }
        ],
        "status": "OK"
    },
    "Goa": {
        "results": [
            {
                "formatted_address": "Goa, India",
                "geometry": {
                    "location": {
                        "lat": 15.2993,
                        "lng": 74.1240
                    }
                },
                "place_id": "ChIJQ9-Q-Q-s-zsR_wJ-0d-0Z8c",
            }
        ],
        "status": "OK"
    }
}

@mcp.tool()
def get_geocode(place_name: str) -> Dict[str, Any]:
    """
    Retrieves mock geolocation data for a specific place name.

    Args:
        place_name: The name of the place to geocode.

    Returns:
        A dictionary with the geocode data, or a ZERO_RESULTS status if not found.
    """
    logger.info(f">>> 🛠️ Tool: 'get_geocode' called for '{place_name}'")
    return GEOCODE_DATA.get(place_name, {"results": [], "status": "ZERO_RESULTS"})

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8084)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8084),
        )
    )