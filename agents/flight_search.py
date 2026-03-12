"""
Flight Search Agent
Searches and scores flight options based on constraints.
In production: integrates with Amadeus or Skyscanner API.
For demo: returns realistic mocked results.
"""

from dataclasses import dataclass


@dataclass
class FlightOption:
    airline: str
    origin: str
    destination: str
    outbound_duration: str
    return_duration: str
    stops: int
    price_per_person: float
    total_price: float
    departure_date: str
    highlights: list
    carrier_type: str  # "full-service" | "budget"


MOCK_FLIGHTS = {
    "Japan": [
        FlightOption("Japan Airlines", "JFK", "NRT", "14h 05m", "13h 20m", 0,
                     780, 0, "Apr 3", ["Non-stop", "Award-winning in-flight meal", "Generous baggage"], "full-service"),
        FlightOption("United Airlines", "JFK", "NRT", "15h 30m", "14h 45m", 1,
                     620, 0, "Apr 3", ["1 stop via SFO", "Good legroom", "Standard service"], "full-service"),
        FlightOption("ANA", "JFK", "NRT", "14h 10m", "13h 25m", 0,
                     810, 0, "Apr 5", ["Non-stop", "Excellent service", "5-star Skytrax"], "full-service"),
        FlightOption("Korean Air", "JFK", "NRT", "16h 40m", "15h 55m", 1,
                     530, 0, "Apr 4", ["1 stop via ICN", "Good value", "Reliable carrier"], "full-service"),
    ],
    "Italy": [
        FlightOption("ITA Airways", "JFK", "FCO", "9h 15m", "10h 30m", 0,
                     680, 0, "Apr 3", ["Non-stop to Rome", "Italian cuisine onboard", "Direct arrival"], "full-service"),
        FlightOption("Lufthansa", "JFK", "FCO", "11h 50m", "13h 05m", 1,
                     510, 0, "Apr 3", ["1 stop via FRA", "Reliable service", "Good value"], "full-service"),
        FlightOption("Ryanair", "LGW", "CIA", "2h 30m", "2h 40m", 0,
                     95, 0, "Apr 4", ["Budget carrier", "No frills", "Very affordable"], "budget"),
    ],
    "Thailand": [
        FlightOption("Thai Airways", "JFK", "BKK", "21h 30m", "22h 15m", 1,
                     850, 0, "Apr 3", ["1 stop via BKK hub", "Royal Silk business option", "Reliable"], "full-service"),
        FlightOption("Emirates", "JFK", "BKK", "20h 45m", "21h 30m", 1,
                     780, 0, "Apr 4", ["1 stop via DXB", "Award-winning service", "ICE entertainment"], "full-service"),
        FlightOption("AirAsia X", "LAX", "BKK", "19h 00m", "20h 30m", 1,
                     420, 0, "Apr 5", ["Budget long-haul", "No frills", "Cheapest option"], "budget"),
    ],
}

DEFAULT_FLIGHTS = [
    FlightOption("Delta Airlines", "JFK", "DEST", "10h 00m", "11h 00m", 1,
                 650, 0, "Apr 3", ["1 stop", "Standard service"], "full-service"),
    FlightOption("American Airlines", "JFK", "DEST", "9h 30m", "10h 30m", 1,
                 580, 0, "Apr 4", ["1 stop", "Good value"], "full-service"),
    FlightOption("Spirit Airlines", "JFK", "DEST", "12h 00m", "13h 00m", 2,
                 290, 0, "Apr 5", ["Budget carrier", "2 stops", "Lowest cost"], "budget"),
]


def search_flights(constraints: dict, price_ceiling: float = None,
                   allow_budget_carriers: bool = False, date_flex_days: int = 0) -> list:
    """
    Return ranked flight options.
    price_ceiling: max per-person price — tightened on retry.
    allow_budget_carriers: unlocked on retry cycle 2+.
    date_flex_days: expand search window on retry.
    """
    destination = constraints.get("destination", "Unknown")
    travelers = constraints.get("travelers", 1)
    budget = constraints.get("budget_usd", 3000)

    if price_ceiling is None:
        price_ceiling = (budget * 0.50) / max(travelers, 1)

    flights = MOCK_FLIGHTS.get(destination, DEFAULT_FLIGHTS)

    results = []
    for f in flights:
        if not allow_budget_carriers and f.carrier_type == "budget":
            continue
        if f.price_per_person <= price_ceiling:
            f_copy = FlightOption(**f.__dict__)
            f_copy.total_price = f.price_per_person * travelers
            results.append(f_copy)

    # Sort by total price ascending (best value first)
    results.sort(key=lambda x: x.total_price)
    return results
