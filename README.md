```markdown
# Travel Planning Agent

A multi-agent AI workflow that turns a high-level travel request into a budget-aware flight and hotel plan using orchestration, parallel sub-agents, and constraint-based optimization.

## Problem

Travel planning is a multi-step decision workflow. Users do not just want flights or hotels in isolation. They want a plan that balances budget, timing, quality, and preferences.

Most tools force users to manage these tradeoffs manually across disconnected search flows. This project explores how an agentic system can break travel planning into specialized tasks and return a structured recommendation.

## What it does

Given a request like:

> "Plan a 10-day trip to Japan in April under $3,000 for 2 people, focused on food and culture."

the system:

- parses user intent and extracts constraints
- dispatches tasks to specialist agents
- searches hotels and flights in parallel
- combines results into viable trip options
- optimizes for budget, quality, and user preferences
- returns a ranked travel plan with alternatives

## System Architecture

User Goal
→ Trip Planner Agent
→ Hotel Search Agent + Flight Search Agent
→ Budget Optimizer
→ Final Travel Plan

### Components

**Trip Planner Agent**
Parses the request, extracts constraints, and routes tasks to sub-agents.

**Hotel Search Agent**
Finds and ranks accommodation options based on budget, location, and reviews.

**Flight Search Agent**
Searches routes, compares layovers and schedule tradeoffs, and identifies best-value flights.

**Budget Optimizer**
Combines hotel and flight candidates and scores them against total budget and user preferences.

**Final Output Layer**
Returns a structured itinerary, budget summary, and alternative options.

## Stack

- LangGraph
- GPT-4o
- Travel and accommodation APIs
- Constraint-based scoring logic
- Streamlit

## Why this project matters

This project explores a broader AI product pattern: turning an ambiguous user goal into a structured workflow handled by multiple specialized agents.

The same architecture can apply to other domains such as healthcare advocacy, insurance navigation, financial planning, and enterprise decision support.

## Demo

![Architecture](assets/travel-planning-agent.png)

## Next Steps

- Add activity planning agent
- Add conversational revision loop
- Improve scoring transparency
- Build evaluation framework for itinerary quality
- Add saved preference memory

## Run Locally

```bash
git clone <repo-url>
cd travel-planning-agent
pip install -r requirements.txt
streamlit run app.py
```
