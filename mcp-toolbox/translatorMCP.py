import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Translator MCP Server 🌐")

# Mock translation data
TRANSLATIONS = {
    "en": {
        "es": {"hello": "hola", "goodbye": "adiós"},
        "fr": {"hello": "bonjour", "goodbye": "au revoir"}
    }
}

@mcp.tool()
def translate_text(text: str, source_language: str, target_language: str) -> Dict[str, Any]:
    """
    Translates text from one language to another.

    Args:
        text: The text to translate.
        source_language: The source language code (e.g., 'en').
        target_language: The target language code (e.g., 'es').

    Returns:
        A dictionary with the translation details.
    """
    logger.info(f">>> 🛠️ Tool: 'translate_text' called for '{text}' from '{source_language}' to '{target_language}'")
    translated_text = TRANSLATIONS.get(source_language, {}).get(target_language, {}).get(text.lower(), "Translation not found")
    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language
    }

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8087)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8087),
        )
    )