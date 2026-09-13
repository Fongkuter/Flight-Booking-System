import hashlib
import re

from database.database import Database


class UserService:

    def __init__(self):

        self.db = Database()

    def hash_password(self, password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    def is_valid_email(self, email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(
            pattern,
            email
        ) is not None

    def is_valid_phone(self, phone):

        pattern = r"^(0|\+84)[0-9]{9,10}$"

        return re.match(
            pattern,
            phone
        ) is not None

    def register_customer(
        self,
        full_name,
        email,
        phone,
        username,
        password,
        confirm_password
    ):

        full_name = full_name.strip()
        email = email.strip()
        phone = phone.strip()
        username = username.strip()

        if not full_name:

            return False, "Vui lòng nhập họ và tên."

        if not email:

            return False, "Vui lòng nhập email."

        if not phone:

            return False, "Vui lòng nhập số điện thoại."

        if not username:

            return False, "Vui lòng nhập tên đăng nhập."

        if not password:

            return False, "Vui lòng nhập mật khẩu."

        if not confirm_password:

            return False, "Vui lòng xác nhận mật khẩu."

        if not self.is_valid_email(email):

            return False, "Email không hợp lệ."

        if not self.is_valid_phone(phone):

            return False, "Số điện thoại không hợp lệ."
            
        if len(username) < 4:

            return False, (
                "Tên đăng nhập phải có ít nhất 4 ký tự."
            )

        if len(password) < 6:

            return False, (
                "Mật khẩu phải có ít nhất 6 ký tự."
            )

        if password != confirm_password:

            return False, (
                "Mật khẩu xác nhận không khớp."
            )


        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                SELECT user_id
                FROM users
                WHERE username = ?
            """, (username,))

            existing_username = cursor.fetchone()

            if existing_username:

                return False, (
                    "Tên đăng nhập đã tồn tại."
                )

            cursor.execute("""
                SELECT user_id
                FROM users
                WHERE email = ?
            """, (email,))

            existing_email = cursor.fetchone()

            if existing_email:

                return False, (
                    "Email đã được sử dụng."
                )

            password_hash = self.hash_password(
                password
            )

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
                full_name,
                email,
                phone,
                username,
                password_hash,
                "customer"
            ))


            conn.commit()

            return True, (
                "Đăng ký tài khoản thành công."
            )

        except Exception as e:


            conn.rollback()

            return False, (
                f"Lỗi đăng ký tài khoản: {str(e)}"
            )

        finally:

            conn.close()
