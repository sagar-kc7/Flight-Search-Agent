from state import FlightSearchState


def approval_node(state: FlightSearchState) -> dict:
    """Human-in-the-loop checkpoint. Prints the pick and asks for confirmation
    before anything gets emailed. In LangGraph you'd normally use an
    `interrupt()` here for a real pause/resume flow - this simple version
    just blocks on input() for now, which is fine while running locally."""
    deal = state["best_deal"]
    if deal is None:
        print("No flights found. Nothing to approve.")
        return {"approved": False}

    print(f"\nBest deal found: {deal['price']} {deal['currency']} on {deal['airline']} (source: {deal['source']})")
    answer = input("Send this deal via email? [y/n]: ").strip().lower()
    return {"approved": answer == "y"}
