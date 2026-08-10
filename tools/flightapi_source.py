import requests

FLIGHTAPI_BASE = "https://api.flightapi.io/onewaytrip"


def search_flights_flightapi(api_key: str, origin: str, destination: str,
                              departure_date: str, max_results: int = 5) -> list[dict]:
    """
    departure_date must be YYYY-MM-DD and in the future.
    Returns a list of normalized offers:
    {"source": "flightapi", "price": float, "currency": str, "airline": str, "raw": {...}}
    """
    url = f"{FLIGHTAPI_BASE}/{api_key}/{origin}/{destination}/{departure_date}/1/0/0/Economy/USD"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    itineraries = data.get("itineraries", [])
    legs = {leg["id"]: leg for leg in data.get("legs", [])}
    carriers = {c["id"]: c.get("name", "unknown") for c in data.get("carriers", [])}

    if not itineraries:
        raise RuntimeError(f"No itineraries returned by FlightAPI: {data}")

    offers = []
    for itin in itineraries[:max_results]:
        pricing_options = itin.get("pricing_options", [])
        if not pricing_options:
            continue
        price = pricing_options[0]["price"]["amount"]

        # resolve airline name via the first leg's marketing carrier id
        airline = "unknown"
        leg_id = itin.get("leg_ids", [None])[0]
        leg = legs.get(leg_id)
        if leg and leg.get("marketing_carrier_ids"):
            carrier_id = leg["marketing_carrier_ids"][0]
            airline = carriers.get(carrier_id, "unknown")

        offers.append({
            "source": "flightapi",
            "price": float(price),
            "currency": "USD",
            "airline": airline,
            "raw": itin,
        })
    return offers