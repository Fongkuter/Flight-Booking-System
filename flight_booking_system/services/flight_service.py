from database.database import Database


class FlightService:

    def __init__(self):
        self.db = Database()

    def search_flights(
        self,
        departure_airport=None,
        arrival_airport=None,
        flight_date=None
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                flight_id,
                flight_code,
                departure_airport,
                arrival_airport,
                departure_time,
                arrival_time,
                flight_date,
                price,
                available_seats,
                status
            FROM flights
            WHERE 1 = 1
        """

        params = []

        # Tìm theo điểm đi
        if departure_airport:
            query += """
                AND departure_airport = ?
            """
            params.append(departure_airport.strip().upper())

        # Tìm theo điểm đến
        if arrival_airport:
            query += """
                AND arrival_airport = ?
            """
            params.append(arrival_airport.strip().upper())

        # Tìm theo ngày
        if flight_date:
            query += """
                AND flight_date = ?
            """
            params.append(flight_date.strip())

        # Chỉ lấy chuyến bay đang hoạt động
        query += """
            AND status = 'scheduled'
        """

        # Chỉ lấy chuyến còn ghế
        query += """
            AND available_seats > 0
        """

        # Sắp xếp theo giờ khởi hành
        query += """
            ORDER BY flight_date, departure_time
        """

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            flights = []

            for row in rows:
                flights.append(dict(row))

            return True, flights

        except Exception as e:
            return False, f"Lỗi tìm kiếm chuyến bay: {str(e)}"

        finally:
            conn.close()

    def get_flight_by_id(self, flight_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    flight_id,
                    flight_code,
                    departure_airport,
                    arrival_airport,
                    departure_time,
                    arrival_time,
                    flight_date,
                    price,
                    available_seats,
                    status
                FROM flights
                WHERE flight_id = ?
            """, (flight_id,))

            row = cursor.fetchone()

            if row is None:
                return False, "Không tìm thấy chuyến bay."

            return True, dict(row)

        except Exception as e:
            return False, f"Lỗi lấy thông tin chuyến bay: {str(e)}"

        finally:
            conn.close()
