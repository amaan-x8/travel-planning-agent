"""
Trip Planner Agent
Parses user intent and extracts structured constraints from a natural language travel request.
"""

import re


def parse_request(user_input: str) -> dict:
    """
    Extract structured constraints from a free-text travel request.
    In production this would call an LLM with a structured output schema.
    For demo purposes, uses pattern matching + sensible defaults.
    """
    constraints = {
        "destination": _extract_destination(user_input),
        "duration_days": _extract_duration(user_input),
        "budget_usd": _extract_budget(user_input),
        "travelers": _extract_travelers(user_input),
        "interests": _extract_interests(user_input),
        "raw_request": user_input,
    }
    return constraints


def _extract_destination(text: str) -> str:
    destinations = ["japan", "italy", "france", "thailand", "spain", "mexico", "greece", "portugal", "bali", "new york", "london", "tokyo", "paris"]
    text_lower = text.lower()
    for dest in destinations:
        if dest in text_lower:
            return dest.title()
    return "Unknown Destination"


def _extract_duration(text: str) -> int:
    match = re.search(r"(\d+)[- ]day", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d+) (days|nights|weeks)", text, re.IGNORECASE)
    if match:
        n = int(match.group(1))
        if "week" in match.group(2).lower():
            return n * 7
        return n
    return 7  # default


def _extract_budget(text: str) -> int:
    match = re.search(r"\$([0-9,]+)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    match = re.search(r"(\d+)[k]", text, re.IGNORECASE)
    if match:
        return int(match.group(1)) * 1000
    return 3000  # default


def _extract_travelers(text: str) -> int:
    match = re.search(r"(\d+) (people|person|traveler|adult)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    if "couple" in text.lower() or "two of us" in text.lower():
        return 2
    return 1


def _extract_interests(text: str) -> list:
    interest_map = {
        "food": ["food", "eat", "cuisine", "restaurant", "dining"],
        "culture": ["culture", "history", "museum", "temple", "art"],
        "adventure": ["hike", "trek", "outdoor", "adventure", "nature"],
        "beach": ["beach", "ocean", "coast", "swim", "snorkel"],
        "nightlife": ["nightlife", "bar", "club", "party"],
        "shopping": ["shop", "market", "mall", "boutique"],
    }
    found = []
    text_lower = text.lower()
    for interest, keywords in interest_map.items():
        if any(kw in text_lower for kw in keywords):
            found.append(interest)
    return found if found else ["sightseeing"]
