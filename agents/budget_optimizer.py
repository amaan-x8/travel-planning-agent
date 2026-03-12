"""
Budget Optimizer
Combines hotel + flight candidates, scores combinations, and enforces budget constraints.
Implements retry loop: if total cost exceeds budget, tightens constraints and re-dispatches.
"""

from dataclasses import dataclass
from agents.hotel_search import search_hotels, HotelOption
from agents.flight_search import search_flights, FlightOption

MAX_RETRIES = 3


@dataclass
class TripCombination:
    hotel: HotelOption
    flight: FlightOption
    total_cost: float
    within_budget: bool
    score: float
    retry_cycle: int


def optimize(constraints: dict) -> dict:
    """
    Main optimization loop. Returns the best trip combination found,
    along with metadata about how many retry cycles were needed.
    """
    budget = constraints.get("budget_usd", 3000)
    duration = constraints.get("duration_days", 7)
    travelers = constraints.get("travelers", 1)

    retry_cycle = 0
    history = []

    # Tightening parameters per retry cycle
    hotel_ceiling_factor  = [0.40, 0.30, 0.22]   # % of budget for hotels
    flight_ceiling_factor = [0.50, 0.40, 0.33]    # % of budget for flights (per person)
    allow_budget_carriers = [False, False, True]
    date_flex_days        = [0, 3, 5]

    best_result = None

    while retry_cycle < MAX_RETRIES:
        hotel_ceiling  = (budget * hotel_ceiling_factor[retry_cycle]) / max(duration, 1)
        flight_ceiling = (budget * flight_ceiling_factor[retry_cycle]) / max(travelers, 1)

        hotels  = search_hotels(constraints, price_ceiling=hotel_ceiling)
        flights = search_flights(
            constraints,
            price_ceiling=flight_ceiling,
            allow_budget_carriers=allow_budget_carriers[retry_cycle],
            date_flex_days=date_flex_days[retry_cycle],
        )

        combinations = _score_combinations(
            hotels, flights, budget, travelers, duration, retry_cycle
        )

        history.append({
            "cycle": retry_cycle + 1,
            "hotels_found": len(hotels),
            "flights_found": len(flights),
            "combinations_scored": len(combinations),
            "hotel_ceiling": round(hotel_ceiling),
            "flight_ceiling_per_person": round(flight_ceiling),
            "allow_budget_carriers": allow_budget_carriers[retry_cycle],
        })

        within_budget = [c for c in combinations if c.within_budget]

        if within_budget:
            best_result = within_budget[0]
            best_result.retry_cycle = retry_cycle
            break

        # No combo within budget — store best-effort for fallback
        if combinations and (best_result is None or combinations[0].total_cost < best_result.total_cost):
            best_result = combinations[0]
            best_result.retry_cycle = retry_cycle

        retry_cycle += 1

    return {
        "best": best_result,
        "retry_history": history,
        "retries_needed": retry_cycle,
        "budget_met": best_result.within_budget if best_result else False,
    }


def _score_combinations(hotels, flights, budget, travelers, duration, retry_cycle):
    combos = []
    for hotel in hotels[:3]:   # top 3 hotels
        for flight in flights[:3]:   # top 3 flights
            total = hotel.total_price + flight.total_price
            within = total <= budget

            # Scoring: penalize over-budget, reward rating + low cost
            cost_score   = max(0, 1 - (total / budget))
            quality_score = (hotel.rating / 5.0) * 0.4
            value_score  = cost_score * 0.6

            score = quality_score + value_score if within else (quality_score + value_score) * 0.5

            combos.append(TripCombination(
                hotel=hotel,
                flight=flight,
                total_cost=round(total, 2),
                within_budget=within,
                score=round(score, 3),
                retry_cycle=retry_cycle,
            ))

    combos.sort(key=lambda x: (-x.within_budget, -x.score))
    return combos
