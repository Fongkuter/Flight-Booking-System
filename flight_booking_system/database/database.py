import os
import sqlite3
from typing import Optional, Dict, Any, List

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False
    MySQLError = Exception


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.is_mysql = False
            cls._instance.connection = None
        return cls._instance

    def __init__(self, host="localhost", user="root", password="", database="flight_booking_db", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.sqlite_path = os.path.join(os.path.dirname(__file__), "flight_booking.db")

    def connect(self) -> bool:
        """
        Ưu tiên kết nối MySQL. Nếu MySQL chưa bật hoặc chưa cài đặt driver,
        hệ thống sẽ tự động chuyển sang dùng SQLite (flight_booking.db) để đảm bảo ứng dụng luôn chạy mượt mà.
        """
        if HAS_MYSQL:
            try:
                # 1. Tạo database nếu chưa có trên MySQL Server
                temp_conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    connection_timeout=3
                )
                cur = temp_conn.cursor()
                cur.execute(f"CREATE DATABASE IF NOT EXISTS \`{self.database}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                cur.close()
                temp_conn.close()

                # 2. Kết nối tới database
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                self.is_mysql = True
                print(f"[Database] Đã kết nối thành công tới MySQL ({self.database}@{self.host})")
                return True
            except Exception as e:
                print(f"[Cảnh báo MySQL]: Không thể kết nối MySQL ({e}). Đang chuyển sang dùng SQLite dự phòng...")

        # Chuyển sang dùng SQLite
        try:
            self.connection = sqlite3.connect(self.sqlite_path)
            self.connection.row_factory = sqlite3.Row
            self.is_mysql = False
            print(f"[Database] Đã kết nối SQLite cơ sở dữ liệu: {self.sqlite_path}")
            return True
        except Exception as e:
            print(f"[Lỗi nghiêm trọng]: Không thể khởi tạo database: {e}")
            return False

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Thực thi câu truy vấn SELECT và trả về danh sách dict"""
        if self.connection is None:
            self.connect()

        # Chuẩn hóa cú pháp tham số giữa MySQL (%s) và SQLite (?)
        if not self.is_mysql:
            query = query.replace("%s", "?")

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        
        if self.is_mysql:
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            return [dict(zip(columns, row)) for row in rows]
        else:
            rows = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in rows]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Thực thi câu lệnh INSERT / UPDATE / DELETE và trả về lastrowid hoặc rowcount"""
        if self.connection is None:
            self.connect()

        if not self.is_mysql:
            query = query.replace("%s", "?")

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def create_tables(self):
        """Khởi tạo tất cả 8 bảng dữ liệu chuẩn hóa 3NF"""
        if self.is_mysql:
            auto_inc = "INT AUTO_INCREMENT PRIMARY KEY"
        else:
            auto_inc = "INTEGER PRIMARY KEY AUTOINCREMENT"

        # Users
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS users (
            id {auto_inc},
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            full_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            role VARCHAR(20) DEFAULT 'customer',
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Airports
        self.execute_update("""
        CREATE TABLE IF NOT EXISTS airports (
            code VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            city VARCHAR(100) NOT NULL,
            country VARCHAR(50) DEFAULT 'Việt Nam'
        );
        """)

        # Airlines
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS airlines (
            id {auto_inc},
            code VARCHAR(10) NOT NULL UNIQUE,
            name VARCHAR(100) NOT NULL,
            logo VARCHAR(10) DEFAULT '✈️'
        );
        """)

        # Airplanes
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS airplanes (
            id {auto_inc},
            code VARCHAR(20) NOT NULL UNIQUE,
            model VARCHAR(50) NOT NULL,
            airline_id INT NOT NULL,
            total_seats INT NOT NULL
        );
        """)

        # Flights
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS flights (
            id {auto_inc},
            flight_number VARCHAR(20) NOT NULL,
            airline_id INT NOT NULL,
            airplane_id INT NOT NULL,
            departure_airport VARCHAR(10) NOT NULL,
            arrival_airport VARCHAR(10) NOT NULL,
            departure_time VARCHAR(30) NOT NULL,
            arrival_time VARCHAR(30) NOT NULL,
            duration_minutes INT NOT NULL,
            base_price DECIMAL(12, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Scheduled'
        );
        """)

        # Seats
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS seats (
            id {auto_inc},
            flight_id INT NOT NULL,
            seat_number VARCHAR(10) NOT NULL,
            class_type VARCHAR(20) DEFAULT 'Economy',
            extra_price DECIMAL(12, 2) DEFAULT 0,
            status VARCHAR(20) DEFAULT 'available'
        );
        """)

        # Bookings
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS bookings (
            id {auto_inc},
            booking_code VARCHAR(20) NOT NULL UNIQUE,
            user_id INT NOT NULL,
            flight_id INT NOT NULL,
            passenger_name VARCHAR(100) NOT NULL,
            passenger_id_num VARCHAR(30) NOT NULL,
            passenger_phone VARCHAR(20) NOT NULL,
            passenger_email VARCHAR(100) NOT NULL,
            seat_number VARCHAR(10) NOT NULL,
            baggage_kg INT DEFAULT 7,
            total_amount DECIMAL(12, 2) NOT NULL,
            payment_status VARCHAR(20) DEFAULT 'Pending',
            booking_status VARCHAR(20) DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Payments
        self.execute_update(f"""
        CREATE TABLE IF NOT EXISTS payments (
            id {auto_inc},
            booking_id INT NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            method VARCHAR(30) DEFAULT 'VietQR',
            status VARCHAR(20) DEFAULT 'Success',
            transaction_ref VARCHAR(100) NOT NULL,
            payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    def seed_initial_data(self):
        """Khởi tạo tài khoản mẫu và các chuyến bay ban đầu"""
        users = self.execute_query("SELECT id FROM users WHERE username = %s", ("admin",))
        if not users:
            self.execute_update("""
            INSERT INTO users (username, password_hash, email, full_name, phone, role, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ("admin", "admin123", "admin@skywings.vn", "Quản Trị Viên Hệ Thống", "0901234567", "admin", "active"))
            self.execute_update("""
            INSERT INTO users (username, password_hash, email, full_name, phone, role, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ("quocvuong", "123456", "quocvuong.hqv@gmail.com", "Hoàng Quốc Vương", "0988776655", "customer", "active"))

        airports = self.execute_query("SELECT code FROM airports")
        if not airports:
            for code, name, city in [
                ("HAN", "Sân bay Quốc tế Nội Bài", "Hà Nội"),
                ("SGN", "Sân bay Quốc tế Tân Sơn Nhất", "TP. Hồ Chí Minh"),
                ("DAD", "Sân bay Quốc tế Đà Nẵng", "Đà Nẵng"),
                ("CXR", "Sân bay Quốc tế Cam Ranh", "Nha Trang"),
                ("PQC", "Sân bay Quốc tế Phú Quốc", "Phú Quốc"),
            ]:
                self.execute_update("INSERT INTO airports (code, name, city) VALUES (%s, %s, %s)", (code, name, city))

        airlines = self.execute_query("SELECT id FROM airlines")
        if not airlines:
            for code, name, logo in [
                ("VN", "Vietnam Airlines", "🇻🇳"),
                ("VJ", "Vietjet Air",),
                ("QH", "Bamboo Airways",),
                ("VU", "Vietravel Airlines",),
            ]:
                self.execute_update("INSERT INTO airlines (code, name, logo) VALUES (%s, %s, %s)", (code, name, logo))

        planes = self.execute_query("SELECT id FROM airplanes")
        if not planes:
            for code, model, aid, seats in [
                ("VN-A861", "Boeing 787-9 Dreamliner", 1, 274),
                ("VJ-A690", "Airbus A321neo", 2, 230),
                ("QH-A899", "Airbus A320-200", 3, 180),
            ]:
                self.execute_update("INSERT INTO airplanes (code, model, airline_id, total_seats) VALUES (%s, %s, %s, %s)", (code, model, aid, seats))

        flights = self.execute_query("SELECT id FROM flights")
        if not flights:
            for f_num, a_id, ap_id, dep, arr, dep_t, arr_t, dur, price in [
                ("VN214", 1, 1, "SGN", "HAN", "2026-09-20 07:30", "2026-09-20 09:40", 130, 1850000.0),
                ("VJ138", 2, 2, "SGN", "HAN", "2026-09-20 09:15", "2026-09-20 11:25", 130, 1290000.0),
                ("QH220", 3, 3, "SGN", "HAN", "2026-09-20 14:00", "2026-09-20 16:10", 130, 1550000.0),
                ("VN126", 1, 1, "HAN", "DAD", "2026-09-20 08:00", "2026-09-20 09:20", 80, 1250000.0),
                ("VJ501", 2, 2, "HAN", "DAD", "2026-09-20 11:30", "2026-09-20 12:50", 80, 890000.0),
            ]:
                self.execute_update("""
                INSERT INTO flights (flight_number, airline_id, airplane_id, departure_airport, arrival_airport, departure_time, arrival_time, duration_minutes, base_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (f_num, a_id, ap_id, dep, arr, dep_t, arr_t, dur, price))
