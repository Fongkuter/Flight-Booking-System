import re

def validate_email(email: str) -> bool:
    """Kiểm tra định dạng email hợp lệ"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại Việt Nam (10 số, bắt đầu bằng 0)"""
    pattern = r"^0[3|5|7|8|9][0-9]{8}$"
    return bool(re.match(pattern, phone.strip()))

def validate_id_number(id_num: str) -> bool:
    """Kiểm tra số CCCD (12 số) hoặc Hộ chiếu"""
    clean_id = id_num.strip()
    return len(clean_id) >= 8 and (clean_id.isalnum())

def validate_username(username: str) -> bool:
    """Tên đăng nhập từ 3 đến 30 ký tự, không dấu cách"""
    pattern = r"^[a-zA-Z0-9_]{3,30}$"
    return bool(re.match(pattern, username.strip()))
