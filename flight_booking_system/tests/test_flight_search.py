from database.database import Database
from services.flight_service import FlightService


def main():
    # Khởi tạo database và dữ liệu mẫu
    db = Database()
    db.create_tables()
    db.create_demo_flights()

    flight_service = FlightService()

    print("\n===== TÌM KIẾM CHUYẾN BAY =====")

    departure = input("Nhập sân bay đi: ").strip()
    arrival = input("Nhập sân bay đến: ").strip()
    flight_date = input("Nhập ngày bay (YYYY-MM-DD): ").strip()

    success, result = flight_service.search_flights(
        departure_airport=departure,
        arrival_airport=arrival,
        flight_date=flight_date
    )

    print("\n===== KẾT QUẢ =====")

    if not success:
        print(result)
        return

    if len(result) == 0:
        print("Không tìm thấy chuyến bay phù hợp.")
        return

    print(f"Tìm thấy {len(result)} chuyến bay:\n")

    for flight in result:
        print("-" * 60)
        print("Mã chuyến bay :", flight["flight_code"])
        print(
            "Chặng bay     :",
            flight["departure_airport"],
            "->",
            flight["arrival_airport"]
        )
        print("Ngày bay      :", flight["flight_date"])
        print(
            "Thời gian     :",
            flight["departure_time"],
            "-",
            flight["arrival_time"]
        )
        print(
            "Giá vé        :",
            f"{flight['price']:,.0f}",
            "VND"
        )
        print("Ghế còn       :", flight["available_seats"])
        print("Trạng thái    :", flight["status"])


if __name__ == "__main__":
    main()
