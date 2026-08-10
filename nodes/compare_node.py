import os
import json
from langchain_groq import ChatGroq
from state import FlightSearchState

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.environ["GROQ_API_KEY"],
    temperature=0,
)


def _summarize_offer(offer: dict, index: int) -> str:
    """Build a short text description of one offer for the LLM prompt."""
    raw = offer.get("raw", {})
    flights = raw.get("flights", [])  # present for serpapi offers
    layovers = raw.get("layovers", [])

    if flights:
        duration = raw.get("total_duration", "unknown")
        stops = len(layovers)
        return (f"[{index}] {offer['source']} - {offer['airline']} - "
                f"${offer['price']} - {stops} stop(s) - {duration} min total")
    else:
        # flightapi or other sources without detailed leg data
        return f"[{index}] {offer['source']} - {offer['airline']} - ${offer['price']}"


def compare_node(state: FlightSearchState) -> dict:
    offers = state["raw_results"]
    if not offers:
        return {"best_deal": None}

    if len(offers) == 1:
        return {"best_deal": offers[0]}

    listing = "\n".join(_summarize_offer(o, i) for i, o in enumerate(offers))

    prompt = f"""You are picking the best flight deal from the options below.
Consider price as the primary factor, but prefer fewer stops and shorter
duration when prices are close (within ~10%).

Options:
{listing}

Respond with ONLY a JSON object, no other text: {{"best_index": <int>, "reason": "<short reason>"}}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    try:
        parsed = json.loads(content)
        best_index = parsed["best_index"]
        best = dict(offers[best_index])
        best["reason"] = parsed.get("reason", "")
    except (json.JSONDecodeError, KeyError, IndexError):
        # fallback: if the LLM response is unparseable, fall back to cheapest
        best = dict(min(offers, key=lambda o: o["price"]))
        best["reason"] = "fallback: LLM response unparseable, picked cheapest"

    return {"best_deal": best}