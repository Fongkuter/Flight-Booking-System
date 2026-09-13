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
