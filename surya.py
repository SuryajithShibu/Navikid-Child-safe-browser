import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QPushButton, QWidget, QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QDateTime
import csv
import os
from Dashboard   import Dashboard 
# List of allowed websites
ALLOWED_SITES = ["https://www.kidfriendlysite.com", "https://www.education.com",]

# Main Browser Class
class ChildSafeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Child Safe Browser")
        self.setGeometry(300, 150, 800, 600)
        self.dashboard = None

        self.browser = QWebEngineView()
        home_url = QUrl.fromLocalFile(os.path.abspath("home.html"))
        self.browser.setUrl(home_url)

        # Set layout
        layout = QVBoxLayout()
        nav_bar=QHBoxLayout()

         # Initialize the home button
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        nav_bar.addWidget(home_button)

         
        # Add Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.browser.back)  
        nav_bar.addWidget(back_button)

        # Add Forward button
        forward_button = QPushButton("Forward")
        forward_button.clicked.connect(self.browser.forward)  
        nav_bar.addWidget(forward_button)


        # Add Refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.browser.reload)  
        nav_bar.addWidget(refresh_button)

        layout.addLayout(nav_bar)
 
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or Search")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        layout.addWidget(self.url_bar)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



        # Initialize the dashboard button
        dashboard_button = QPushButton("Show Dashboard")
        dashboard_button.clicked.connect(self.show_dashboard)
        layout.addWidget(dashboard_button) 

        #Log file to record browsing history
        self.log_file = "browsing_log.csv"
        self.initialize_log()
        
        #reset button
        reset_button=QPushButton("Reset Graph")
        reset_button.clicked.connect(self.reset_graph)
        layout.addWidget(reset_button)

        



    def navigate_to_url(self):
        url = self.url_bar.text()
        if self.is_site_allowed(url):
            self.browser.setUrl(QUrl(url))
            self.log_activity(url)

            if self.dashboard:
                self.dashboard.update_dashboard()     
        else:
            self.show_block_message()

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def is_site_allowed(self, url):
        """Allow only pre-approved websites."""
        return any(site in url for site in ALLOWED_SITES)

    def show_block_message(self):
        """Show message when site is blocked."""
        QMessageBox.warning(self, "Blocked", "This site is not allowed for kids!")


    def initialize_log(self):
        """Create log file if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "URL"])

    def log_activity(self, url):
        """Log the visited URL with timestamp."""
        timestamp = QDateTime.currentDateTime().toString()
        with open(self.log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, url])

        if self.dashboard:
            self.dashboard.update_dashboard()

    def show_dashboard(self):
        """Launch the dashboard window."""
        if not self.dashboard:
           self.dashboard = Dashboard (self.log_file)
        self.dashboard.show() 

    def reset_graph(self):
       """Clear the log file and reset the graph."""
       with open(self.log_file, mode="w", newline="") as file:
         writer = csv.writer(file)
         writer.writerow(["Timestamp", "URL"])

      

       if self.dashboard:
        self.dashboard.update_dashboard()

            

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = ChildSafeBrowser()
    browser.show()
    sys.exit(app.exec_())
