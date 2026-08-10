from state import FlightSearchState


def compare_node(state: FlightSearchState) -> dict:
    """Pick the cheapest valid offer. No LLM needed for pure price comparison -
    keep it simple logic; you can swap this for LLM-based reasoning later if you
    want to factor in things like layovers or airline preference."""
    if not state["raw_results"]:
        return {"best_deal": None}

    best = min(state["raw_results"], key=lambda offer: offer["price"])
    return {"best_deal": best}
