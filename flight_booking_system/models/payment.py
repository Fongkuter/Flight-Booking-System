from dataclasses import dataclass
from typing import Optional

@dataclass
class Payment:
    id: Optional[int]
    booking_id: int
    amount: float
    method: str
    status: str
    transaction_ref: str
    payment_time: Optional[str] = None
