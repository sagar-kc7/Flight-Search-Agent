import operator
from typing import TypedDict, Optional, List, Dict, Any, Annotated


class FlightSearchState(TypedDict):
    # Inputs
    origin: str
    destination: str
    departure_date: str  # YYYY-MM-DD
    return_date: Optional[str]

    # Working data - Annotated with operator.add so parallel nodes MERGE
    # their results into these lists instead of overwriting each other.
    raw_results: Annotated[List[Dict[str, Any]], operator.add]
    errors: Annotated[List[str], operator.add]

    # Output of comparison
    best_deal: Optional[Dict[str, Any]]

    # Human-in-the-loop / final step
    approved: bool
    email_sent: bool
