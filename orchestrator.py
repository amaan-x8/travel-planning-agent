"""
Orchestrator
Coordinates the full agent pipeline:
  1. Trip Planner  — parse intent
  2. Hotel Search  — find accommodation (parallel with flights in prod)
  3. Flight Search — find routes
  4. Budget Optimizer — score, enforce budget, retry if needed
  5. Output — structured final plan
"""

from agents.trip_planner import parse_request
from agents.budget_optimizer import optimize


def run_pipeline(user_input: str) -> dict:
    """
    End-to-end pipeline. Returns a structured result dict.
    """
    # Step 1: Parse intent
    constraints = parse_request(user_input)

    # Steps 2–4: Search + optimize (with retry loop)
    result = optimize(constraints)

    # Step 5: Build final output
    return _build_output(constraints, result)


def _build_output(constraints: dict, result: dict) -> dict:
    best = result["best"]

    if best is None:
        return {
            "success": False,
            "message": "Could not find any options matching your request. Try relaxing your budget or dates.",
            "constraints": constraints,
            "retry_history": result["retry_history"],
        }

    hotel  = best.hotel
    flight = best.flight

    # Build daily itinerary stub based on interests
    interests = constraints.get("interests", ["sightseeing"])
    days      = constraints.get("duration_days", 7)
    dest      = constraints.get("destination", "your destination")

    itinerary = _generate_itinerary(dest, days, interests)

    return {
        "success": True,
        "budget_met": result["budget_met"],
        "retries_needed": result["retries_needed"],
        "retry_history": result["retry_history"],
        "constraints": constraints,
        "recommendation": {
            "hotel": {
                "name": hotel.name,
                "location": hotel.location,
                "stars": hotel.stars,
                "price_per_night": hotel.price_per_night,
                "total_hotel_cost": hotel.total_price,
                "rating": hotel.rating,
                "highlights": hotel.highlights,
                "neighborhood": hotel.neighborhood,
            },
            "flight": {
                "airline": flight.airline,
                "route": f"{flight.origin} → {flight.destination}",
                "outbound": flight.outbound_duration,
                "return": flight.return_duration,
                "stops": flight.stops,
                "price_per_person": flight.price_per_person,
                "total_flight_cost": flight.total_price,
                "departure_date": flight.departure_date,
                "highlights": flight.highlights,
            },
            "total_cost": best.total_cost,
            "budget": constraints.get("budget_usd", 3000),
            "remaining_budget": round(constraints.get("budget_usd", 3000) - best.total_cost, 2),
            "score": best.score,
        },
        "itinerary": itinerary,
    }


def _generate_itinerary(destination: str, days: int, interests: list) -> list:
    """Generate a simple day-by-day itinerary stub."""
    templates = {
        "food": ["Visit a local food market", "Take a cooking class", "Dine at a top-rated local restaurant", "Street food tour"],
        "culture": ["Explore the old town", "Visit the national museum", "Tour a historic temple or cathedral", "Guided walking tour"],
        "adventure": ["Day hike to a scenic viewpoint", "Bike tour around the city", "Kayaking or water sports excursion"],
        "beach": ["Beach day at the most popular local beach", "Sunset cruise", "Snorkeling excursion"],
        "shopping": ["Morning at the local market", "Browse boutiques in the design district"],
        "sightseeing": [f"Top landmarks of {destination}", "Panoramic viewpoint visit", "Neighbourhood exploration walk"],
    }

    activities = []
    for interest in interests:
        activities.extend(templates.get(interest, []))

    # Pad with sightseeing if needed
    while len(activities) < days:
        activities.extend(templates["sightseeing"])

    itinerary = []
    for i in range(days):
        label = "Arrival & settle in" if i == 0 else ("Departure day" if i == days - 1 else activities[i % len(activities)])
        itinerary.append({"day": i + 1, "activity": label})

    return itinerary
