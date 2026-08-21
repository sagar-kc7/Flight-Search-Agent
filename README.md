# Flight Price Agent - LangGraph

A LangGraph agent that searches flight prices across multiple real sources,
picks the best deal, asks for your approval, and emails it to you.

## Architecture

```
        START
       /      \
  serpapi   flightapi   <- run in parallel (2 real sources)
       \      /
       compare            <- picks cheapest offer
          |
       approval           <- human-in-the-loop (y/n prompt)
        /   \
  send_email  END
       |
      END
```

- `search_serpapi`: real Google Flights data via SerpApi (free tier: 100 searches/month)
- `search_site_b`: real data via FlightAPI.io (free tier: 30 credits, no card required)
- State merging: since both search nodes write to `raw_results` in parallel,
  `state.py` uses `Annotated[List, operator.add]` so LangGraph appends
  results instead of one node's write clobbering another's.

## Setup

1. Get a free SerpApi key: https://serpapi.com/manage-api-key
2. Get a free FlightAPI.io key: https://api.flightapi.io/register
3. `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `cp .env.example .env` and fill in your keys (SerpApi, FlightAPI, Groq if you add LLM
   reasoning later, and SMTP for email - use a Gmail App Password, not your real password)
6. Edit the `initial_state` in `main.py` with your origin/destination/date
7. `python main.py`

## Next steps

1. Add LLM-based reasoning (Groq) to `compare_node` to factor in layovers,
   duration, or legroom instead of pure cheapest-price logic
2. Add a LangGraph checkpointer (e.g. `SqliteSaver`) so state persists across runs -
   lets you dedupe "already seen this deal" across multiple executions
3. Wrap each tool (SerpApi search, FlightAPI search, email) as its own MCP server,
   and swap the LangGraph tool calls to hit them over MCP instead of calling the
   Python functions directly
