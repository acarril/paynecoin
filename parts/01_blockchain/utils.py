from hashlib import sha256

def compute_hash(data: bytes) -> str:
    return sha256(data).hexdigest()