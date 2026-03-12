# Travel Planning Agent

A multi-agent travel planning system that searches flights and hotels in parallel
and optimizes combinations within a user's budget.

---

## Product Problem

Travel search is fragmented across flights, hotels, and budgets.  
Users repeatedly restart searches when the total cost exceeds their budget.

---

## Solution

A multi-agent planner that:

1. Parses travel intent
2. Searches flights and hotels in parallel
3. Scores possible trip combinations
4. Automatically retries with tighter constraints if the budget is exceeded

---

## Outcome

Reduces manual search loops and produces viable itineraries faster by automatically
optimizing travel combinations within a defined budget.

---

## Architecture

Orchestrator Agent  
Hotel Search Agent  
Flight Search Agent  
Budget Optimizer  

Retry loop triggers if total trip cost exceeds the user's budget.

---

## Tech Stack

Python  
LangGraph  
Claude / GPT-4o  
Streamlit
