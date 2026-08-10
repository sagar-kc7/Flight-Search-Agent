from state import FlightSearchState
from tools.serpapi_source import search_flights_serpapi
from tools.mock_source import search_flights_mock


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
    """Placeholder second source (mock). Swap for a real scraper later."""
    try:
        results = search_flights_mock(
            "site_b", state["origin"], state["destination"],
            state["departure_date"], state.get("return_date"),
        )
        return {"raw_results": results}
    except Exception as e:
        return {"errors": [f"site_b: {e}"]}


def search_site_c_node(state: FlightSearchState) -> dict:
    """Placeholder third source (mock). Swap for a real scraper later."""
    try:
        results = search_flights_mock(
            "site_c", state["origin"], state["destination"],
            state["departure_date"], state.get("return_date"),
        )
        return {"raw_results": results}
    except Exception as e:
        return {"errors": [f"site_c: {e}"]}
