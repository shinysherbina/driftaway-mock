import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Budget MCP Server 💰")

# Mock budget data
BUDGETS = {}
EXPENSES = {}

@mcp.tool()
def create_budget(trip_id: int, total_amount: float) -> Dict[str, Any]:
    """
    Creates a new budget for a trip.

    Args:
        trip_id: The ID of the trip.
        total_amount: The total budget amount.

    Returns:
        A dictionary with the created budget details.
    """
    logger.info(f">>> 🛠️ Tool: 'create_budget' called for trip ID '{trip_id}'")
    budget_id = f"budget_{trip_id}"
    BUDGETS[budget_id] = {"trip_id": trip_id, "total_amount": total_amount}
    return {
        "budget_id": budget_id,
        "trip_id": trip_id,
        "total_amount": total_amount,
        "status": "created"
    }

@mcp.tool()
def add_expense(budget_id: str, category: str, amount: float) -> Dict[str, Any]:
    """
    Adds an expense to a budget.

    Args:
        budget_id: The ID of the budget.
        category: The category of the expense.
        amount: The amount of the expense.

    Returns:
        A dictionary with the added expense details.
    """
    logger.info(f">>> 🛠️ Tool: 'add_expense' called for budget ID '{budget_id}'")
    expense_id = f"exp_{len(EXPENSES) + 1}"
    EXPENSES[expense_id] = {"budget_id": budget_id, "category": category, "amount": amount}
    return {
        "expense_id": expense_id,
        "budget_id": budget_id,
        "category": category,
        "amount": amount,
        "status": "added"
    }

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8082)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8082),
        )
    )