"""
Real flight data source using SerpApi's Google Flights engine.
Docs: https://serpapi.com/google-flights-api
Free tier: 100 searches/month.
"""
import os
import requests

SERPAPI_URL = "https://serpapi.com/search"


def search_flights_serpapi(origin: str, destination: str, departure_date: str,
                            return_date: str | None = None, max_results: int = 5) -> list[dict]:
    """
    Returns a list of normalized offers:
    {"source": "serpapi_google_flights", "price": float, "currency": "USD", "airline": str, "raw": {...}}
    """
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "currency": "USD",
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    # Google Flights requires a trip type; if no return_date, treat as one-way
    if return_date:
        params["return_date"] = return_date
        params["type"] = "1"  # round trip
    else:
        params["type"] = "2"  # one-way

    response = requests.get(SERPAPI_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    # SerpApi returns "best_flights" and "other_flights" - combine and take cheapest N
    candidates = data.get("best_flights", []) + data.get("other_flights", [])
    if not candidates:
        raise RuntimeError(f"No flights returned by SerpApi: {data.get('error', 'unknown response shape')}")

    offers = []
    for item in candidates[:max_results]:
        price = item.get("price")
        if price is None:
            continue
        first_leg = item["flights"][0]
        airline = first_leg.get("airline", "unknown")
        offers.append({
            "source": "serpapi_google_flights",
            "price": float(price),
            "currency": "USD",
            "airline": airline,
            "raw": item,
        })
    return offers
