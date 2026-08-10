from state import FlightSearchState
from tools.serpapi_source import search_flights_serpapi
from tools.flightapi_source import search_flights_flightapi
import os

def search_serpapi_node(state: FlightSearchState) -> dict:
    """Real source (SerpApi Google Flights). On failure, record the error
    instead of crashing the graph.
    Returns only the NEW items - the state's operator.add reducer appends them."""
    try:
        results = search_flights_serpapi(
            state["origin"], state["destination"],
            state["departure_date"], state.get("return_date"),
        )
        return {"raw_results": results}
    except Exception as e:
        return {"errors": [f"serpapi: {e}"]}

def search_site_b_node(state: FlightSearchState) -> dict:
    """Real source: FlightAPI.io"""
    try:
        results = search_flights_flightapi(
            api_key=os.environ["FLIGHTAPI_KEY"],
            origin=state["origin"],
            destination=state["destination"],
            departure_date=state["departure_date"],
        )
        return {"raw_results": results}
    except Exception as e:
        return {"errors": [f"flightapi: {e}"]}
