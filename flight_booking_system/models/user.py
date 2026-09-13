class User:
    
    def __init__(
        self,
        user_id=None,
        full_name="",
        email="",
        phone="",
        username="",
        password_hash="",
        role="customer"
    ):

        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password_hash = password_hash
        self.role = role
