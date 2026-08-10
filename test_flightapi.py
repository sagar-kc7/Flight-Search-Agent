from dotenv import load_dotenv
load_dotenv()
import os

from tools.flightapi_source import search_flights_flightapi

results = search_flights_flightapi(
    api_key=os.environ["FLIGHTAPI_KEY"],
    origin="KTM",
    destination="DXB",
    departure_date="2026-09-15",
)

for r in results:
    print(r["price"], r["currency"], r["airline"], r["source"])