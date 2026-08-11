"""
MCP server exposing SerpApi Google Flights search as a tool.
Run standalone with: python mcp_servers/serpapi_server.py
"""
import sys
import os

# allow importing from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

from tools.serpapi_source import search_flights_serpapi

mcp = FastMCP("serpapi-flights")


@mcp.tool()
def search_flights(origin: str, destination: str, departure_date: str, return_date: str = "") -> list[dict]:
    """
    Search flight prices via SerpApi's Google Flights engine.

    Args:
        origin: 3-letter IATA airport code (e.g. "KTM")
        destination: 3-letter IATA airport code (e.g. "DXB")
        departure_date: date in YYYY-MM-DD format
        return_date: optional return date in YYYY-MM-DD format, leave empty for one-way
    """
    return search_flights_serpapi(
        origin, destination, departure_date,
        return_date if return_date else None,
    )


if __name__ == "__main__":
    mcp.run()