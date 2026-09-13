class Flight:
    def __init__(
        self,
        flight_id=None,
        flight_code="",
        departure_airport="",
        arrival_airport="",
        departure_time="",
        arrival_time="",
        flight_date="",
        price=0,
        available_seats=0,
        status="scheduled"
    ):
        self.flight_id = flight_id
        self.flight_code = flight_code
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.flight_date = flight_date
        self.price = price
        self.available_seats = available_seats
        self.status = status
