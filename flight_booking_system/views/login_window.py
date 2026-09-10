from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập")
        self.setMinimumSize(420, 280)
        self.setStyleSheet("font-size: 14px;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setFixedWidth(340)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)

        title_label = QLabel("ĐĂNG NHẬP")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        account_row = QHBoxLayout()
        account_label = QLabel("Tài khoản:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("")
        account_row.addWidget(account_label)
        account_row.addWidget(self.username_input)

        password_row = QHBoxLayout()
        password_label = QLabel("Mật khẩu:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("")
        password_row.addWidget(password_label)
        password_row.addWidget(self.password_input)

        self.login_button = QPushButton("Đăng nhập")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setFixedHeight(34)

        register_hint = QLabel("Chưa có tài khoản?")
        register_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.register_button = QPushButton("Đăng ký")
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.setFixedWidth(120)

        container_layout.addWidget(title_label)
        container_layout.addLayout(account_row)
        container_layout.addLayout(password_row)
        container_layout.addWidget(self.login_button)
        container_layout.addWidget(register_hint)
        container_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(container)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        print(f"Tài khoản: {username}")
        print(f"Mật khẩu: {password}")
