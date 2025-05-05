import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QApplication
from surya import ChildSafeBrowser
from blockchain import Blockchain

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(400, 200, 500, 300)

        # Background Image
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 500, 400)
        pixmap = QPixmap("/Users/suryajithshibu/__pycache__/Images.png")  
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        self.background_label.setScaledContents(True)

        # Central Widget
        self.container = QWidget(self)
        self.setCentralWidget(self.container)

        
        # Create the layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        title = QLabel("Secure Browser Login")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: Black")
        layout.addWidget(title)
        #bold
        bold_font = QFont()
        bold_font.setBold(True)

        # Adding Space Before Login Button
        spacer = QSpacerItem(15, 15, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Username Label and Input
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial Display", 15))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        
        # Password Label and Input
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial Display", 15))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet(self.get_input_style())
    
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Adding Space Before Login Button
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 30))
        self.login_button.setStyleSheet(self.get_button_style())
        self.login_button.setStyleSheet("background-color: green; color: white;")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Set layout to QWidget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Hardcoded User Data (Will replace with blockchain later)
        self.users = {"parent": "password123", "child": "childpassword"}
        #Blockchain Logger
        self.blockchain = Blockchain()

    def get_input_style(self):
        """Returns the style for input fields."""
        return (
            "padding: 10px; "
            "border: 2px solid #2e86de; "
            "border-radius: 8px; "
            "font-size: 14px;"
        )
    
    def get_button_style(self):
        """Returns the style for the login button."""
        return (
            "background-color: #2e86de; "
            "color: white; "
            "padding: 10px; "
            "border: none; "
            "border-radius: 8px;"
        )


    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username in self.users and self.users[username] == password:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.blockchain.add_login_attempt(username,"Success")
            self.close()  # Close the login window
            self.browser_window = ChildSafeBrowser()
            self.browser_window.show()

    
            # Here you will launch the browser (we'll add this part later)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
            self.blockchain.add_login_attempt(username,"Failed")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
