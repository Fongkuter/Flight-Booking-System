import random
import string
from datetime import datetime

def generate_pnr(length: int = 6) -> str:
    """Tạo mã đặt chỗ PNR gồm 6 ký tự chữ và số ngẫu nhiên (vd: VN8A2K)"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))

def generate_transaction_id() -> str:
    """Tạo mã giao dịch thanh toán"""
    return f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"

def format_currency_vn(amount: float) -> str:
    """Định dạng tiền tệ VNĐ (vd: 1.850.000 đ)"""
    try:
        return f"{int(amount):,}".replace(",", ".") + " đ"
    except Exception:
        return f"{amount} đ"

def calculate_total_price(base_price: float, seat_number: str, baggage_kg: int) -> float:
    """Tính tổng tiền bao gồm phụ thu hạng ghế và hành lý mua thêm"""
    extra_seat = 0.0
    try:
        row_num = int("".join(filter(str.isdigit, seat_number)))
        if row_num <= 3:
            extra_seat = 600000.0  # Hạng Thương Gia
    except ValueError:
        pass

    baggage_fee = 0.0
    if baggage_kg == 20:
        baggage_fee = 220000.0
    elif baggage_kg == 30:
        baggage_fee = 350000.0
    elif baggage_kg == 40:
        baggage_fee = 480000.0

    return base_price + extra_seat + baggage_fee
