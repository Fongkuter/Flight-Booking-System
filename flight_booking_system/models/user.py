from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    email: str
    full_name: str
    phone: str
    role: str = "customer" # 'customer' hoặc 'admin'
    status: str = "active" # 'active' hoặc 'blocked'
    created_at: Optional[str] = None

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_active(self) -> bool:
        return self.status == "active"
