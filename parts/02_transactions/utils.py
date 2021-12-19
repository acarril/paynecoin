from hashlib import sha256
import json

def compute_hash(data: bytes) -> str:
    return sha256(data).hexdigest()

def generate_transaction_data(sender_address, recipient_address, amount) -> dict:
    return {
        'sender': sender_address,
        'recipient': recipient_address,
        'amount': amount
    }

def convert_transaction_data_to_bytes(transaction_data: dict):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"] = str(transaction_data["sender"])
    new_transaction_data["recipient"] = str(transaction_data["recipient"])
    new_transaction_data["amount"] = str(transaction_data["amount"])
    return json.dumps(new_transaction_data, indent=2).encode('utf-8')