"""
MCP server exposing the email-sending tool.
Run standalone with: python mcp_servers/email_server.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

from tools.email_tool import send_deal_email

mcp = FastMCP("email-sender")


@mcp.tool()
def send_flight_deal_email(price: float, currency: str, airline: str, source: str,
                            origin: str, destination: str, departure_date: str) -> str:
    """
    Send an email with the best flight deal found.

    Args:
        price: the price of the deal
        currency: currency code, e.g. "USD"
        airline: airline name or code
        source: which data source found this deal
        origin: origin airport code
        destination: destination airport code
        departure_date: departure date YYYY-MM-DD
    """
    deal = {"price": price, "currency": currency, "airline": airline, "source": source}
    send_deal_email(deal, origin, destination, departure_date)
    return "Email sent successfully"


if __name__ == "__main__":
    mcp.run()