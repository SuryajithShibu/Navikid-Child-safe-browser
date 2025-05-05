import os
import json
import hashlib
from datetime import datetime

class Blockchain:
    def __init__(self, blockchain_file="login_blockchain.json"):
        self.blockchain_file = blockchain_file  # Set the attribute here first
        self.chain = self.load_blockchain()  # Now it will correctly load the blockchain
        self.cloud_folder = "CloudStorage"

        # Create the folder if it doesn't exist
        os.makedirs(self.cloud_folder, exist_ok=True)

    def create_block(self, data, previous_hash):
        """Creates a new block and adds it to the chain."""
        block = {
            'index': len(self.chain),
            'data': data,
            'timestamp': str(datetime.now()),
            'previous_hash': previous_hash,
            'hash': self.hash_block(data + previous_hash)
        }
        self.chain.append(block)
        self.save_blockchain()
        self.upload_to_cloud(block)
        return block

    def hash_block(self, data):
        """Creates a SHA-256 hash of the given data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def add_login_attempt(self, username, status):
        """Adds a login attempt as a new block."""
        data = f"Username: {username}, Status: {status}"
        previous_hash = self.chain[-1]['hash'] if self.chain else '0'
        self.create_block(data, previous_hash)

    def save_blockchain(self):
        """Saves the blockchain to a file."""
        try:
            with open(self.blockchain_file, "w") as file:
                json.dump(self.chain, file, indent=4)
            print("✅ Blockchain saved successfully.")
        except Exception as e:
            print(f"❌ Failed to save blockchain: {e}")

    def load_blockchain(self):
        """Loads the blockchain from a file if it exists."""
        if os.path.exists(self.blockchain_file):
            with open(self.blockchain_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("❌ Error decoding blockchain file. Starting a new blockchain.")
                    return []
        return []

    def upload_to_cloud(self, block):
        """Save the block as a JSON file to the 'CloudStorage' folder."""
        filename = f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        filepath = os.path.join(self.cloud_folder, filename)
        
        try:
            with open(filepath, "w") as file:
                json.dump(block, file, indent=4)
            print(f"✅ Successfully saved {filename} to simulated cloud storage.")
        except Exception as e:
            print(f"❌ Failed to save log to cloud: {e}")
