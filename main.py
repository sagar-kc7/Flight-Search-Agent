from dotenv import load_dotenv
load_dotenv()

from graph import build_graph

def main():
    app = build_graph()

    initial_state = {
        "origin": "KTM",              # 3-letter IATA code, e.g. Kathmandu
        "destination": "DXB",         # e.g. Dubai
        "departure_date": "2026-09-15",
        "return_date": None,
        "raw_results": [],
        "errors": [],
        "best_deal": None,
        "approved": False,
        "email_sent": False,
    }

    final_state = app.invoke(initial_state)

    print("\n--- Run summary ---")
    print(f"Offers collected: {len(final_state['raw_results'])}")
    if final_state["errors"]:
        print(f"Errors: {final_state['errors']}")
    print(f"Best deal: {final_state['best_deal']}")
    print(f"Email sent: {final_state['email_sent']}")


if __name__ == "__main__":
    main()
