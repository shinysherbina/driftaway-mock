import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Culture MCP Server 🏛️")

# Mock culture data
CULTURE_DATA = {
    "Munnar, Kerala": {
        "etiquette": "Dress modestly, especially when visiting religious sites. Remove shoes before entering homes or religious sites. Use your right hand for eating and transactions.",
        "languages": ["Malayalam", "Tamil", "English", "Hindi"],
        "phrases": [
            {"phrase": "Hello", "translation": "Namaskaram"},
            {"phrase": "Thank you", "translation": "Nanni"},
            {"phrase": "How are you?", "translation": "Sukhamaano?"},
            {"phrase": "What is your name?", "translation": "Ninte perenthaanu?"},
        ],
    },
    "Darjeeling, West Bengal": {
        "etiquette": "Greet with 'Namaste'. Dress modestly. Remove shoes in religious places. Ask for permission before taking photos of people.",
        "languages": ["Nepali", "Bengali", "Hindi", "English"],
        "phrases": [
            {"phrase": "Hello", "translation": "Namaste"},
            {"phrase": "Thank you", "translation": "Dhanyabaad"},
            {"phrase": "How are you?", "translation": "Tapailai Kasto Cha?"},
            {"phrase": "What is your name?", "translation": "Tapaiko naam ke ho?"},
        ],
    },
    "Agra, Uttar Pradesh": {
        "etiquette": "Dress modestly, especially at religious sites. Remove shoes before entering temples or mosques. Be prepared for crowds.",
        "languages": ["Hindi", "Urdu", "Braj Bhasha", "English"],
        "phrases": [
            {"phrase": "Hello", "translation": "Namaste"},
            {"phrase": "Thank you", "translation": "Dhanyavaad"},
            {"phrase": "How are you?", "translation": "Aap kaise hain?"},
            {"phrase": "What is your name?", "translation": "Aapka naam kya hai?"},
        ],
    },
    "Goa": {
        "etiquette": "'Susegad' (relaxed) attitude. Dress modestly away from the beach. Respect religious sites.",
        "languages": ["Konkani", "Marathi", "English", "Hindi", "Portuguese"],
        "phrases": [
            {"phrase": "Hello", "translation": "Deu boro dis dium"},
            {"phrase": "Thank you", "translation": "Deu borem korum"},
            {"phrase": "How are you?", "translation": "Tum Ko so asa?"},
            {"phrase": "What is your name?", "translation": "Tujem naum kitay?"},
        ],
    },
}


@mcp.tool()
def get_cultural_info(place_name: str) -> Dict[str, Any]:
    """
    Gets cultural information for a specific place.

    Args:
        place_name: The name of the place to get cultural information for.

    Returns:
        A dictionary with the cultural information.
    """
    logger.info(f">>> 🛠️ Tool: 'get_cultural_info' called for '{place_name}'")
    return CULTURE_DATA.get(
        place_name, {"etiquette": "Information not found.", "languages": [], "phrases": []}
    )

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8083)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8083),
        )
    )