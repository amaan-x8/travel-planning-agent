"""
Hotel Search Agent
Searches and ranks hotel options based on constraints.
In production: integrates with Booking.com API or similar.
For demo: returns realistic mocked results.
"""

from dataclasses import dataclass


@dataclass
class HotelOption:
    name: str
    location: str
    stars: int
    price_per_night: float
    total_price: float
    rating: float
    highlights: list
    neighborhood: str


# Mocked hotel data by destination
MOCK_HOTELS = {
    "Japan": [
        HotelOption("Shinjuku Granbell Hotel", "Shinjuku, Tokyo", 4, 120, 0, 4.5,
                    ["Walking distance to Shinjuku Gyoen", "Stylish design rooms", "Rooftop bar"], "Shinjuku"),
        HotelOption("APA Hotel Asakusa", "Asakusa, Tokyo", 3, 75, 0, 4.1,
                    ["Near Senso-ji Temple", "Compact Japanese-style rooms", "Coin laundry"], "Asakusa"),
        HotelOption("The Ritz-Carlton Tokyo", "Midtown, Tokyo", 5, 480, 0, 4.9,
                    ["45th floor panoramic views", "Award-winning spa", "Butler service"], "Midtown"),
        HotelOption("Dormy Inn Shibuya", "Shibuya, Tokyo", 3, 85, 0, 4.3,
                    ["Natural hot spring bath", "Late-night ramen service", "Great Shibuya access"], "Shibuya"),
    ],
    "Italy": [
        HotelOption("Hotel Artemide", "Via Nazionale, Rome", 4, 145, 0, 4.4,
                    ["Steps from Termini station", "Rooftop terrace", "Free Wi-Fi"], "City Center"),
        HotelOption("B&B Colosseum View", "Celio, Rome", 3, 90, 0, 4.2,
                    ["Views of the Colosseum", "Charming family-run", "Local breakfast included"], "Celio"),
        HotelOption("Hotel Hassler Roma", "Trinità dei Monti, Rome", 5, 520, 0, 4.8,
                    ["At the top of Spanish Steps", "Michelin-starred restaurant", "Historic luxury"], "Pinciano"),
    ],
    "Thailand": [
        HotelOption("Chatrium Hotel Riverside", "Riverside, Bangkok", 5, 110, 0, 4.6,
                    ["Stunning Chao Phraya views", "Infinity pool", "Free shuttle boat"], "Riverside"),
        HotelOption("Lub d Bangkok Silom", "Silom, Bangkok", 2, 35, 0, 4.0,
                    ["Social hostel-style", "Central Silom location", "Rooftop pool"], "Silom"),
        HotelOption("Riva Arun Bangkok", "Phra Nakhon, Bangkok", 4, 160, 0, 4.7,
                    ["Views of Wat Arun", "Boutique riverside hotel", "Unique local experience"], "Old Town"),
    ],
}

DEFAULT_HOTELS = [
    HotelOption("City Center Hotel", "Downtown", 4, 110, 0, 4.3,
                ["Central location", "Business amenities", "24hr front desk"], "Downtown"),
    HotelOption("Budget Inn Express", "Midtown", 3, 65, 0, 3.9,
                ["Affordable", "Clean rooms", "Easy transit access"], "Midtown"),
    HotelOption("Grand Luxury Suites", "Old Town", 5, 350, 0, 4.8,
                ["Premium experience", "Fine dining", "Spa and wellness"], "Old Town"),
]


def search_hotels(constraints: dict, price_ceiling: float = None) -> list:
    """
    Return ranked hotel options for the destination and budget.
    price_ceiling: max nightly rate — tightened on retry cycles.
    """
    destination = constraints.get("destination", "Unknown")
    duration = constraints.get("duration_days", 7)
    travelers = constraints.get("travelers", 1)
    budget = constraints.get("budget_usd", 3000)

    # Default ceiling: 40% of total budget / nights / travelers
    if price_ceiling is None:
        price_ceiling = (budget * 0.40) / max(duration, 1)

    hotels = MOCK_HOTELS.get(destination, DEFAULT_HOTELS)

    results = []
    for h in hotels:
        if h.price_per_night <= price_ceiling:
            h_copy = HotelOption(**h.__dict__)
            h_copy.total_price = h.price_per_night * duration * travelers
            results.append(h_copy)

    # Sort by rating descending
    results.sort(key=lambda x: x.rating, reverse=True)
    return results
