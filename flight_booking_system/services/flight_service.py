from typing import List, Dict, Any, Optional
from database.database import Database
from models.flight import Flight

class FlightService:
    def __init__(self):
        self.db = Database()

    def search_flights(self, dep: str, arr: str, date_str: Optional[str] = None) -> List[Dict[str, Any]]:
        query = """
        SELECT f.*, a.name as airline_name, a.logo as airline_logo, ap.model as plane_model
        FROM flights f
        JOIN airlines a ON f.airline_id = a.id
        JOIN airplanes ap ON f.airplane_id = ap.id
        WHERE f.departure_airport = %s AND f.arrival_airport = %s AND f.status != 'Cancelled'
        """
        params = [dep, arr]
        results = self.db.execute_query(query, tuple(params))
        return results

    def get_all_flights(self) -> List[Dict[str, Any]]:
        query = """
        SELECT f.*, a.name as airline_name, a.logo as airline_logo
        FROM flights f
        JOIN airlines a ON f.airline_id = a.id
        ORDER BY f.id DESC
        """
        return self.db.execute_query(query)

    def add_flight(self, flight_number: str, airline_id: int, airplane_id: int,
                   dep: str, arr: str, dep_time: str, arr_time: str,
                   duration: int, price: float) -> int:
        query = """
        INSERT INTO flights (flight_number, airline_id, airplane_id, departure_airport, arrival_airport,
                            departure_time, arrival_time, duration_minutes, base_price, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Scheduled')
        """
        return self.db.execute_update(query, (flight_number, airline_id, airplane_id, dep, arr, dep_time, arr_time, duration, price))

    def update_flight_status(self, flight_id: int, status: str):
        self.db.execute_update("UPDATE flights SET status = %s WHERE id = %s", (status, flight_id))

    def delete_flight(self, flight_id: int):
        self.db.execute_update("DELETE FROM flights WHERE id = %s", (flight_id,))

    def get_occupied_seats(self, flight_id: int) -> List[str]:
        query = "SELECT seat_number FROM bookings WHERE flight_id = %s AND booking_status != 'Cancelled'"
        rows = self.db.execute_query(query, (flight_id,))
        return [r["seat_number"] for r in rows]
