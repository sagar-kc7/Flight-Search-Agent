from langgraph.graph import StateGraph, START, END
from state import FlightSearchState
from nodes.search_nodes import search_serpapi_node, search_site_b_node, search_site_c_node
from nodes.compare_node import compare_node
from nodes.approval_node import approval_node
from nodes.email_node import email_node


def build_graph():
    graph = StateGraph(FlightSearchState)

    graph.add_node("search_serpapi", search_serpapi_node)
    graph.add_node("search_site_b", search_site_b_node)
    graph.add_node("search_site_c", search_site_c_node)
    graph.add_node("compare", compare_node)
    graph.add_node("approval", approval_node)
    graph.add_node("send_email", email_node)

    # Fan-out: all three searches run in parallel from START
    graph.add_edge(START, "search_serpapi")
    graph.add_edge(START, "search_site_b")
    graph.add_edge(START, "search_site_c")

    # Fan-in: all three must finish before compare runs
    graph.add_edge("search_serpapi", "compare")
    graph.add_edge("search_site_b", "compare")
    graph.add_edge("search_site_c", "compare")

    graph.add_edge("compare", "approval")

    # Conditional edge: only email if approved
    def route_after_approval(state: FlightSearchState) -> str:
        return "send_email" if state["approved"] else "__end__"

    graph.add_conditional_edges("approval", route_after_approval, {
        "send_email": "send_email",
        "__end__": END,
    })

    graph.add_edge("send_email", END)

    return graph.compile()
