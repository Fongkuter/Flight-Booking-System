import sqlite3
import os
import hashlib

class Database:
    def __init__(self):
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )
        self.db_path = os.path.join(
            base_dir,
            "flight_booking.db"
        )
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    def create_demo_account(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT user_id
                FROM users
                WHERE username = ?
            """, ("demo",))
            existing_user = cursor.fetchone()
            if existing_user:
                return
            password_hash = hashlib.sha256(
                "123456".encode("utf-8")
            ).hexdigest()
            cursor.execute("""
                INSERT INTO users (
                    full_name,
                    email,
                    phone,
                    username,
                    password_hash,
                    role
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "Nguyễn Văn Demo",
                "demo@gmail.com",
                "0901234567",
                "demo",
                password_hash,
                "customer"
            ))
            conn.commit()
            print("Đã tạo tài khoản demo.")
        except Exception as e:
            conn.rollback()
            print(
                "Lỗi tạo tài khoản demo:",
                e
            )
        finally:
            conn.close()
        def create_demo_flights(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        flights = [
            (
                "VN101",
                "SGN",
                "HAN",
                "07:00",
                "09:10",
                "2026-09-20",
                1500000,
                120,
                "scheduled"
            ),
            (
                "VN102",
                "HAN",
                "SGN",
                "10:00",
                "12:10",
                "2026-09-20",
                1600000,
                100,
                "scheduled"
            ),
            (
                "VN201",
                "SGN",
                "DAD",
                "08:00",
                "09:20",
                "2026-09-20",
                1100000,
                80,
                "scheduled"
            ),
            (
                "VN202",
                "DAD",
                "SGN",
                "14:00",
                "15:20",
                "2026-09-20",
                1150000,
                70,
                "scheduled"
            ),
            (
                "VN301",
                "SGN",
                "HAN",
                "18:30",
                "20:40",
                "2026-09-21",
                1750000,
                90,
                "scheduled"
            ),
        ]

        try:
            for flight in flights:
                cursor.execute("""
                    SELECT flight_id
                    FROM flights
                    WHERE flight_code = ?
                """, (flight[0],))

                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO flights (
                        flight_code,
                        departure_airport,
                        arrival_airport,
                        departure_time,
                        arrival_time,
                        flight_date,
                        price,
                        available_seats,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, flight)

            conn.commit()

            print("Đã tạo dữ liệu chuyến bay mẫu.")

        except Exception as e:
            conn.rollback()
            print("Lỗi tạo chuyến bay mẫu:", e)

        finally:
            conn.close()
