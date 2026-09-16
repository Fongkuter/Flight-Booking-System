from dataclasses import dataclass
from typing import Optional

@dataclass
class Flight:
    id: Optional[int]
    flight_number: str
    airline_id: int
    airplane_id: int
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    base_price: float
    status: str = "Scheduled"
    airline_name: Optional[str] = None
    airline_logo: Optional[str] = None
