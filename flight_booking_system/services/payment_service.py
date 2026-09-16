from typing import Optional
from database.database import Database
from utils.helper import generate_transaction_id

class PaymentService:
    def __init__(self):
        self.db = Database()

    def process_payment(self, booking_id: int, amount: float, method: str = "VietQR") -> str:
        txn = generate_transaction_id()
        query = """
        INSERT INTO payments (booking_id, amount, method, status, transaction_ref)
        VALUES (%s, %s, %s, 'Success', %s)
        """
        self.db.execute_update(query, (booking_id, amount, method, txn))
        return txn

    def get_all_payments(self):
        query = """
        SELECT p.*, b.booking_code, b.passenger_name
        FROM payments p
        JOIN bookings b ON p.booking_id = b.id
        ORDER BY p.id DESC
        """
        return self.db.execute_query(query)
