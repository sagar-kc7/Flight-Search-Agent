# Flight Price Agent

A LangGraph agent that searches flight prices across multiple sources,
picks the best deal, asks for your approval, and emails it to you.

## Architecture

```
        START
       /  |  \
  serpapi site_b site_c   <- run in parallel (3 "sites")
       \  |  /
       compare              <- picks cheapest offer
          |
       approval             <- human-in-the-loop (y/n prompt)
        /   \
  send_email  END
       |
      END
```

- `search_serpapi`: real Google Flights data via SerpApi (free tier: 100 searches/month)
- `search_site_b` / `search_site_c`: currently MOCK data (tools/mock_source.py).
  Replace with real scrapers (Playwright) or another API once the graph works end to end.
- State merging: since all 3 search nodes write to `raw_results` in parallel,
  `state.py` uses `Annotated[List, operator.add]` so LangGraph appends
  results instead of one node's write clobbering another's.

## Setup

1. Get a free SerpApi key: https://serpapi.com/manage-api-key
2. `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and fill in your keys (SerpApi, Anthropic if you add LLM
   reasoning later, and SMTP for email - use a Gmail App Password, not your real password)
5. Edit the `initial_state` in `main.py` with your origin/destination/date
6. `python main.py`

## Next steps (once this works)

1. Replace `tools/mock_source.py` calls with real scrapers or a second API
2. Swap `compare_node`'s simple `min()` logic for an LLM call if you want to factor
   in things like layovers, baggage, or airline preference - good place to practice
   tool-calling with reasoning instead of pure logic
3. Add a LangGraph checkpointer (e.g. `SqliteSaver`) so state persists across runs -
   lets you dedupe "already seen this deal" across multiple executions
4. Wrap each tool (Amadeus search, email) as its own MCP server, and swap the
   LangGraph tool calls to hit them over MCP instead of calling the Python
   functions directly
