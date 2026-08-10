from state import FlightSearchState
from tools.email_tool import send_deal_email


def email_node(state: FlightSearchState) -> dict:
    if not state["approved"] or state["best_deal"] is None:
        return {"email_sent": False}

    send_deal_email(
        state["best_deal"], state["origin"], state["destination"], state["departure_date"]
    )
    print("Email sent.")
    return {"email_sent": True}
