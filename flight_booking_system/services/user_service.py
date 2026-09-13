import hashlib
import re

from database.database import Database


class UserService:

    def __init__(self):

        self.db = Database()

    # ==================================================
    # HASH PASSWORD
    # ==================================================

    def hash_password(self, password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    # ==================================================
    # VALIDATE EMAIL
    # ==================================================

    def is_valid_email(self, email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(
            pattern,
            email
        ) is not None

    # ==================================================
    # VALIDATE PHONE
    # ==================================================

    def is_valid_phone(self, phone):

        pattern = r"^(0|\+84)[0-9]{9,10}$"

        return re.match(
            pattern,
            phone
        ) is not None

    # ==================================================
    # REGISTER CUSTOMER
    # ==================================================

    def register_customer(
        self,
        full_name,
        email,
        phone,
        username,
        password,
        confirm_password
    ):

        # ------------------------------------------------
        # 1. Chuẩn hóa dữ liệu
        # ------------------------------------------------

        full_name = full_name.strip()
        email = email.strip()
        phone = phone.strip()
        username = username.strip()

        # ------------------------------------------------
        # 2. Kiểm tra dữ liệu rỗng
        # ------------------------------------------------

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

        # ------------------------------------------------
        # 3. Kiểm tra email
        # ------------------------------------------------

        if not self.is_valid_email(email):

            return False, "Email không hợp lệ."

        # ------------------------------------------------
        # 4. Kiểm tra phone
        # ------------------------------------------------

        if not self.is_valid_phone(phone):

            return False, "Số điện thoại không hợp lệ."

        # ------------------------------------------------
        # 5. Kiểm tra username
        # ------------------------------------------------

        if len(username) < 4:

            return False, (
                "Tên đăng nhập phải có ít nhất 4 ký tự."
            )

        # ------------------------------------------------
        # 6. Kiểm tra password
        # ------------------------------------------------

        if len(password) < 6:

            return False, (
                "Mật khẩu phải có ít nhất 6 ký tự."
            )

        # ------------------------------------------------
        # 7. Kiểm tra confirm password
        # ------------------------------------------------

        if password != confirm_password:

            return False, (
                "Mật khẩu xác nhận không khớp."
            )

        # ------------------------------------------------
        # 8. Kết nối database
        # ------------------------------------------------

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:

            # ============================================
            # 9. Kiểm tra username
            # ============================================

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

            # ============================================
            # 10. Kiểm tra email
            # ============================================

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

            # ============================================
            # 11. Hash password
            # ============================================

            password_hash = self.hash_password(
                password
            )

            # ============================================
            # 12. INSERT USER
            # ============================================

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

            # ============================================
            # 13. COMMIT
            # ============================================

            conn.commit()

            return True, (
                "Đăng ký tài khoản thành công."
            )

        except Exception as e:

            # ============================================
            # Nếu lỗi → rollback
            # ============================================

            conn.rollback()

            return False, (
                f"Lỗi đăng ký tài khoản: {str(e)}"
            )

        finally:

            # ============================================
            # Đóng database connection
            # ============================================

            conn.close()
