from typing import List, Dict, Any, Optional
from database.database import Database
from utils.helper import generate_pnr

class BookingService:
    def __init__(self):
        self.db = Database()

    def create_booking(self, user_id: int, flight_id: int, passenger_name: str,
                       passenger_id_num: str, passenger_phone: str, passenger_email: str,
                       seat_number: str, baggage_kg: int, total_amount: float) -> str:
        pnr = generate_pnr()
        query = """
        INSERT INTO bookings (booking_code, user_id, flight_id, passenger_name, passenger_id_num,
                             passenger_phone, passenger_email, seat_number, baggage_kg,
                             total_amount, payment_status, booking_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Paid', 'Confirmed')
        """
        self.db.execute_update(query, (
            pnr, user_id, flight_id, passenger_name, passenger_id_num,
            passenger_phone, passenger_email, seat_number, baggage_kg, total_amount
        ))
        return pnr

    def get_user_bookings(self, user_id: int) -> List[Dict[str, Any]]:
        query = """
        SELECT b.*, f.flight_number, f.departure_airport, f.arrival_airport, f.departure_time
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.user_id = %s
        ORDER BY b.id DESC
        """
        return self.db.execute_query(query, (user_id,))

    def get_all_bookings(self) -> List[Dict[str, Any]]:
        query = """
        SELECT b.*, f.flight_number, f.departure_airport, f.arrival_airport, f.departure_time
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        ORDER BY b.id DESC
        """
        return self.db.execute_query(query)

    def cancel_booking(self, booking_id: int) -> bool:
        """Hủy vé và giải phóng chỗ ngồi"""
        self.db.execute_update("UPDATE bookings SET booking_status = 'Cancelled', payment_status = 'Cancelled' WHERE id = %s", (booking_id,))
        return True
