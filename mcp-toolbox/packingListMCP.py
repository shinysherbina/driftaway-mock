import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Packing List MCP Server 🧳")

import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Packing List MCP Server 🧳")


@mcp.tool()
def generate_packing_list(
    destination: str,
    start_date: str,
    end_date: str,
    weather_summary: str,
    activity_tags: List[str],
    user_preferences: List[str],
) -> Dict[str, List[str]]:
    """
    You are a travel assistant helping a user prepare for a trip.
    Use the following context to generate a personalized packing list.
    Include essential items, optional extras, and gear based on weather and planned activities.

    Args:
        destination: The destination of the trip.
        start_date: The start date of the trip.
        end_date: The end date of the trip.
        weather_summary: A summary of the weather forecast (e.g. "cold and rainy", "hot and humid").
        activity_tags: A list of planned activities (e.g. hiking, beach, temple visits).
        user_preferences: A list of user preferences (e.g. budget travel, eco-friendly, luxury).

    Returns:
        A dictionary with the personalized packing list, grouped by category.
    """
    logger.info(f">>> 🛠️ Tool: 'generate_packing_list' called for destination '{destination}'")

    # Base packing list
    packing_list = {
        "clothing": ["Underwear", "Socks", "T-shirts", "Pants/Shorts"],
        "gear": ["Phone and charger", "Power bank", "Headphones"],
        "documents": ["Passport/ID", "Visa (if required)", "Tickets", "Hotel reservations"],
        "extras": ["Book/e-reader", "Snacks"],
    }

    # Add items based on weather
    if "cold" in weather_summary:
        packing_list["clothing"].extend(["Jacket", "Sweater", "Beanie", "Gloves"])
    if "rainy" in weather_summary:
        packing_list["clothing"].append("Raincoat")
        packing_list["gear"].append("Umbrella")
    if "hot" in weather_summary:
        packing_list["clothing"].extend(["Shorts", "Tank tops", "Sun hat"])
    if "humid" in weather_summary:
        packing_list["clothing"].append("Lightweight clothing")

    # Add items based on activities
    if "hiking" in activity_tags:
        packing_list["gear"].extend(["Hiking boots", "Backpack", "Water bottle"])
    if "beach" in activity_tags:
        packing_list["clothing"].append("Swimsuit")
        packing_list["gear"].extend(["Sunscreen", "Beach towel", "Sunglasses"])
    if "temple visits" in activity_tags:
        packing_list["clothing"].append("Modest clothing (long pants/skirt, covered shoulders)")

    # Add items based on user preferences
    if "budget travel" in user_preferences:
        packing_list["extras"].append("Reusable water bottle")
    if "eco-friendly" in user_preferences:
        packing_list["extras"].extend(["Reusable shopping bag", "Solid toiletries"])
    if "luxury" in user_preferences:
        packing_list["extras"].append("Portable speaker")

    return packing_list


if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8086)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8086),
        )
    )

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8086)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8086),
        )
    )