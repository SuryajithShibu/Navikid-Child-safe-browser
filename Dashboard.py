import os
import csv
import json
from collections import Counter
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QLabel, QTabWidget
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Dashboard(QWidget):
    def __init__(self, log_file="browsing_log.csv", blockchain_file="login_blockchain.json", cloud_folder="CloudStorage"):
        super().__init__()
        self.log_file = log_file
        self.blockchain_file = blockchain_file
        self.cloud_folder = cloud_folder  # Simulated cloud storage folder
        
        self.setWindowTitle("Child's Web Usage Dashboard")
        self.setGeometry(350, 150, 900, 600)
        
        # Set up layout and tabs
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_web_usage_tab(), "Web Usage")
        self.tabs.addTab(self.create_blockchain_log_tab(), "Login Logs")
        self.tabs.addTab(self.create_cloud_logs_tab(), "Cloud Logs")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
    def create_web_usage_tab(self):
        """Creates the web usage tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Create the Matplotlib figure and canvas
        self.canvas = FigureCanvas(Figure(figsize=(10, 5)))
        layout.addWidget(self.canvas)
        
        tab.setLayout(layout)
        self.plot_data()
        return tab
        
    def plot_data(self):
        """Plot browsing data on the dashboard."""
        timestamps, urls = self.load_data()

        # Define a mapping of URLs to friendly labels and colors
        label_mapping = {
            'https://www.kidfriendlysite.com': ('Kid Friendly', 'red'),
            'https://www.education.com': ('Education', 'skyblue')
        }

        labels = []
        bar_colors = []

        for url in urls:
            if url in label_mapping:
                label, color = label_mapping[url]
                labels.append(label)
                bar_colors.append(color)

        # Count occurrences of each label
        label_counts = Counter(labels)

        ax = self.canvas.figure.subplots()
        ax.clear()

        if not label_counts:
            ax.text(0.5, 0.5, 'No browsing data available', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, fontsize=14)
            self.canvas.draw()
            return

        websites = list(label_counts.keys())
        visits = list(label_counts.values())

        # Plot the bar graph for visited websites only
        bars = ax.bar(websites, visits, color=bar_colors)

        for i, bar in enumerate(bars):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

        ax.set_xlabel("Websites")
        ax.set_ylabel("Visits")
        ax.set_title("Child's Web Usage")
        ax.set_ylim(0, max(visits) + 5)
        self.canvas.draw()

    def load_data(self):
        """Load browsing data from log file."""
        timestamps = []
        urls = []
        try:
            with open(self.log_file, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    timestamps.append(row[0])
                    urls.append(row[1])
        except FileNotFoundError:
            print(f"File {self.log_file} not found.")
        return timestamps, urls
    
    def create_blockchain_log_tab(self):
        """Creates the blockchain log tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        
        logs = self.load_blockchain_logs()
        
        if logs:
            log_display.setText(logs)
        else:
            log_display.setText("No blockchain logs found.")
        
        layout.addWidget(QLabel("Login Attempts (Blockchain Logs):"))
        layout.addWidget(log_display)
        
        tab.setLayout(layout)
        return tab

    def load_blockchain_logs(self):
        """Load and display blockchain logs."""
        try:
            with open(self.blockchain_file, "r") as file:
                blockchain_data = json.load(file)
                logs = ""
                for block in blockchain_data:
                    logs += f"Block {block['index']}\n"
                    logs += f"Data: {block['data']}\n"
                    logs += f"Timestamp: {block['timestamp']}\n"
                    logs += f"Previous Hash: {block['previous_hash']}\n"
                    logs += f"Hash: {block['hash']}\n"
                    logs += "-------------------------------\n\n"
                return logs
        except FileNotFoundError:
            return "No blockchain logs found."
    
    def create_cloud_logs_tab(self):
        """Creates the cloud logs tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        
        logs = self.load_cloud_logs()
        
        if logs:
            log_display.setText(logs)
        else:
            log_display.setText("No cloud logs found.")
        
        layout.addWidget(QLabel("Cloud Logs (Simulated Cloud Storage):"))
        layout.addWidget(log_display)
        
        tab.setLayout(layout)
        return tab

    def load_cloud_logs(self):
        """Load all logs from the CloudStorage folder."""
        logs_text = ""
        
        try:
            for filename in os.listdir(self.cloud_folder):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.cloud_folder, filename)
                    
                    with open(filepath, "r") as file:
                        log_data = json.load(file)
                        logs_text += f"Filename: {filename}\n"
                        logs_text += f"Data: {json.dumps(log_data, indent=4)}\n\n"
            if not logs_text:
                logs_text = "No JSON files found in CloudStorage folder."
        except FileNotFoundError:
            logs_text = "CloudStorage folder not found."
        
        return logs_text


if __name__ == "__main__":
    app = QApplication([])
    dashboard = Dashboard()
    dashboard.show()
    app.exec_()
