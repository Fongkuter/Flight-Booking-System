from dataclasses import dataclass

@dataclass
class Passenger:
    full_name: str
    id_number: str
    phone: str
    email: str
    gender: str = "Ông"
