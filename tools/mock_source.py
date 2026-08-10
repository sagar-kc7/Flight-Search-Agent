"""
Placeholder for a second/third flight source.

SerpApi (Google Flights) is currently the only free, real API wired in
(see serpapi_source.py). This module simulates two more "sites" so you can
build and test the full LangGraph structure (3 parallel search nodes ->
aggregate -> compare) before you've built real scrapers.

TODO (later): replace with Playwright scrapers against a second/third site,
following the same input/output contract as search_flights_serpapi().
"""
import random


def search_flights_mock(source_name: str, origin: str, destination: str,
                         departure_date: str, return_date: str | None = None) -> list[dict]:
    base_price = random.uniform(150, 600)
    offers = []
    for i in range(3):
        offers.append({
            "source": source_name,
            "price": round(base_price + random.uniform(-40, 60), 2),
            "currency": "USD",
            "airline": random.choice(["XY", "ZP", "QR"]),
            "raw": {"note": "mock data - replace with real scraper"},
        })
    return offers
