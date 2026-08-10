from dotenv import load_dotenv
load_dotenv()

from tools.serpapi_source import search_flights_serpapi

results = search_flights_serpapi(
    origin="KTM",
    destination="DXB",
    departure_date="2026-10-09",
)

for r in results:
    print(r["price"], r["currency"], r["airline"], r["source"])