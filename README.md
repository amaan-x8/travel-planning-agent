# Travel Planning Agent

Multi-agent AI system that plans trips within budget using parallel search and optimization.

---

## Product Problem

Travel search is fragmented across flights, hotels, and budgets.  
Users repeatedly restart searches when total cost exceeds their budget.

---

## Solution

A multi-agent planner that:

• Parses travel intent  
• Searches flights and hotels in parallel  
• Scores trip combinations  
• Retries automatically with tighter constraints  

---

## System Architecture

[Your architecture diagram here]

---

## Agent Workflow

User Request  
↓  
Intent Parser  
↓  
Parallel Agent Calls  
↓  
Hotel Agent  
Flight Agent  
↓  
Budget Optimizer  
↓  
Retry Loop (if over budget)

---

## Tech Stack

Python • LangGraph • Claude / GPT-4o • Streamlit
