from dataclasses import dataclass
from typing import Optional

@dataclass
class Ticket:
    ticket_number: str
    booking_code: str
    passenger_name: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    seat_number: str
    class_type: str
    baggage_kg: int
    gate: str = "Gate 04"
    boarding_time: str = "40 phút trước bay"
