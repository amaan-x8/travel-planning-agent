# ✈️ Travel Planning Agent

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-demo--ready-brightgreen)

A multi-agent AI workflow that turns a high-level travel request into a budget-aware flight and hotel plan — using orchestration, parallel sub-agents, constraint-based optimization, and an automatic retry loop.

**[🚀 Live Demo](#)** · **[Architecture](#system-architecture)** · **[Run Locally](#run-locally)**

> Replace the `[🚀 Live Demo](#)` link above with your Streamlit URL after deploying.

---

## Problem

Travel planning is a multi-step decision workflow. Users don't just want flights or hotels in isolation — they want a plan that balances budget, timing, quality, and preferences.

Most tools force users to manage these tradeoffs manually across disconnected search flows. This project explores how an agentic system can break travel planning into specialized tasks, enforce budget constraints automatically, and return a structured recommendation.

---

## What It Does

Given a request like:

> "Plan a 10-day trip to Japan in April under $3,000 for 2 people, focused on food and culture."

The system:
- Parses user intent and extracts structured constraints (destination, budget, duration, travelers, interests)
- Dispatches Hotel Search and Flight Search agents in parallel
- Combines results and scores combinations against the total budget
- **If the total cost exceeds the budget**, triggers a retry loop with tighter constraints (lower price ceilings, alternate dates, budget carriers)
- Returns a ranked travel plan with a day-by-day itinerary

---

## System Architecture

![Architecture](assets/travel-planning-agent.png)

```
User Goal
  └─► Trip Planner Agent        (parse intent, extract constraints)
        ├─► Hotel Search Agent  (find accommodation within ceiling)  ─┐ parallel
        └─► Flight Search Agent (find routes within ceiling)         ─┘
              └─► Budget Optimizer
                    └─► Budget Gate ──── within budget? ──► Final Plan
                              │
                              └── over budget?
                                    └─► Tighten constraints → retry (max 3×)
                                          • Lower hotel nightly cap
                                          • Expand flight date window ±3 days
                                          • Allow budget carriers
                                          • Reduce trip length if needed
```

### Components

| Agent | Role |
|---|---|
| **Trip Planner Agent** | Parses request, extracts constraints (budget, dates, party size, interests) |
| **Hotel Search Agent** | Queries accommodation options; re-runs with tighter ceiling on retry |
| **Flight Search Agent** | Searches routes and date windows; unlocks budget carriers on retry |
| **Budget Optimizer** | Scores hotel × flight combinations; enforces budget gate; triggers retry |
| **Orchestrator** | Coordinates the pipeline; manages retry state and constraint tightening |

---

## Retry Loop

The budget gate is the core differentiator of this architecture. When the optimizer detects that the best available combination exceeds the user's budget:

1. **Cycle 1** — Tighten hotel ceiling to 30% of budget, flight ceiling to 40%
2. **Cycle 2** — Tighten further; unlock budget airline carriers; expand date window ±3 days
3. **Cycle 3** — Reduce trip length; final fallback to lowest-cost options

If budget is still unmet after 3 cycles, the system surfaces the best-effort plan with a cost warning rather than returning an error.

---

## Sample Output

See [`examples/sample_output.md`](examples/sample_output.md) for a full example.

**Input:** "Plan a 10-day trip to Japan in April under $3,000 for 2 people, focused on food and culture."

| | |
|---|---|
| ✈️ Korean Air JFK→NRT (1 stop) | $1,060 total |
| 🏨 APA Hotel Asakusa (3★, 4.1/5) | $1,500 total |
| 💰 Total | **$2,560 of $3,000** |
| 🔁 Retries needed | 1 cycle |

---

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | Python (LangGraph-ready architecture) |
| LLM integration | OpenAI GPT-4o (stubbed for demo) |
| Hotel search | Booking.com API (mocked for demo) |
| Flight search | Amadeus API (mocked for demo) |
| UI / demo | Streamlit |
| Constraint logic | Custom scoring + retry loop |

---

## Repo Structure

```
travel-planning-agent/
├── app.py                    # Streamlit entry point
├── orchestrator.py           # Pipeline coordinator + retry state
├── agents/
│   ├── trip_planner.py       # Intent parsing + constraint extraction
│   ├── hotel_search.py       # Hotel search + ranking
│   ├── flight_search.py      # Flight search + scoring
│   └── budget_optimizer.py   # Constraint satisfaction + retry loop
├── prompts/                  # Agent system prompts (for LLM integration)
├── examples/
│   └── sample_output.md      # Sample request and response
├── assets/
│   └── travel-planning-agent.png  # Architecture diagram
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Known Limitations & Tradeoffs

| Limitation | Reason / Notes |
|---|---|
| Hotel and flight data is mocked | Real API integration (Amadeus, Booking.com) requires paid keys; the architecture is API-ready |
| No LLM calls in demo mode | Intent parsing uses regex; swap `trip_planner.py` for an LLM call to handle ambiguous inputs |
| No memory between sessions | User preferences don't persist; a next step is adding a preference memory layer |
| Retry loop is constraint-based, not learned | A future version could learn which constraint-tightening strategies work best per destination |
| Single itinerary output | The optimizer returns the top-scoring combination; a future version would show 2–3 alternatives side by side |

---

## Why This Project Matters

This explores a broader AI product pattern: turning an ambiguous user goal into a structured workflow handled by multiple specialized agents, with graceful degradation when constraints can't be satisfied.

The same architecture applies to other domains: healthcare navigation, insurance claims, financial planning, enterprise procurement, and legal document review.

---

## Run Locally

```bash
git clone https://github.com/amaan-x8/travel-planning-agent
cd travel-planning-agent
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                              # add real API keys when ready
streamlit run app.py
```

---

## Next Steps

- [ ] Replace mocked data with live Amadeus + Booking.com API calls
- [ ] Add LLM-based intent parsing (GPT-4o structured output)
- [ ] Add activity planning sub-agent
- [ ] Add conversational revision loop ("make it cheaper", "I prefer direct flights")
- [ ] Build evaluation framework for itinerary quality
- [ ] Add user preference memory across sessions
- [ ] Add multi-city / multi-leg trip support

---

## Author

Built by [Amaan](https://github.com/amaan-x8) as a PM portfolio project exploring multi-agent AI system design.
