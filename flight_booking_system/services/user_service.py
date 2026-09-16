from typing import Optional, Dict, Any
from database.database import Database
from models.user import User

class UserService:
    def __init__(self):
        self.db = Database()

    def login(self, username: str, password: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE username = %s"
        results = self.db.execute_query(query, (username.strip(),))
        if not results:
            return None
        row = results[0]
        # Đối chiếu mật khẩu
        if row["password_hash"] == password:
            return User(
                id=row["id"],
                username=row["username"],
                password_hash=row["password_hash"],
                email=row["email"],
                full_name=row["full_name"],
                phone=row["phone"],
                role=row.get("role", "customer"),
                status=row.get("status", "active"),
                created_at=str(row.get("created_at", ""))
            )
        return None

    def register(self, username: str, password: str, email: str, full_name: str, phone: str) -> bool:
        # Kiểm tra trùng lặp
        check = self.db.execute_query("SELECT id FROM users WHERE username = %s OR email = %s", (username.strip(), email.strip()))
        if check:
            return False

        query = """
        INSERT INTO users (username, password_hash, email, full_name, phone, role, status)
        VALUES (%s, %s, %s, %s, %s, 'customer', 'active')
        """
        self.db.execute_update(query, (username.strip(), password, email.strip(), full_name.strip(), phone.strip()))
        return True

    def get_all_users(self):
        return self.db.execute_query("SELECT id, username, full_name, email, phone, role, status, created_at FROM users ORDER BY id DESC")

    def toggle_user_status(self, user_id: int, new_status: str):
        self.db.execute_update("UPDATE users SET status = %s WHERE id = %s", (new_status, user_id))
