"""
Real flight data source using the Amadeus Self-Service API (free test tier).
Docs: https://developers.amadeus.com/self-service/category/flights
"""
import os
from amadeus import Client, ResponseError


def get_amadeus_client() -> Client:
    return Client(
        client_id=os.environ["AMADEUS_CLIENT_ID"],
        client_secret=os.environ["AMADEUS_CLIENT_SECRET"],
    )


def search_flights_amadeus(origin: str, destination: str, departure_date: str,
                            return_date: str | None = None, max_results: int = 5) -> list[dict]:
    """
    Returns a list of normalized offers:
    {"source": "amadeus", "price": float, "currency": str, "airline": str, "raw": {...}}
    """
    client = get_amadeus_client()
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "max": max_results,
    }
    if return_date:
        params["returnDate"] = return_date

    try:
        response = client.shopping.flight_offers_search.get(**params)
    except ResponseError as e:
        raise RuntimeError(f"Amadeus API error: {e}") from e

    offers = []
    for offer in response.data:
        price = offer["price"]["total"]
        currency = offer["price"]["currency"]
        airline = offer["itineraries"][0]["segments"][0]["carrierCode"]
        offers.append({
            "source": "amadeus",
            "price": float(price),
            "currency": currency,
            "airline": airline,
            "raw": offer,
        })
    return offers
