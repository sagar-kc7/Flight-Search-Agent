"""
MCP server exposing FlightAPI.io search as a tool.
Run standalone with: python mcp_servers/flightapi_server.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

from tools.flightapi_source import search_flights_flightapi

mcp = FastMCP("flightapi-flights")


@mcp.tool()
def search_flights(origin: str, destination: str, departure_date: str) -> list[dict]:
    """
    Search flight prices via FlightAPI.io.

    Args:
        origin: 3-letter IATA airport code (e.g. "KTM")
        destination: 3-letter IATA airport code (e.g. "DXB")
        departure_date: date in YYYY-MM-DD format
    """
    return search_flights_flightapi(
        api_key=os.environ["FLIGHTAPI_KEY"],
        origin=origin,
        destination=destination,
        departure_date=departure_date,
    )


if __name__ == "__main__":
    mcp.run()