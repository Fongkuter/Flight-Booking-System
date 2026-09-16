from dataclasses import dataclass
from typing import Optional

@dataclass
class Booking:
    id: Optional[int]
    booking_code: str
    user_id: int
    flight_id: int
    passenger_name: str
    passenger_id_num: str
    passenger_phone: str
    passenger_email: str
    seat_number: str
    baggage_kg: int
    total_amount: float
    payment_status: str = "Pending"
    booking_status: str = "Confirmed"
    created_at: Optional[str] = None
