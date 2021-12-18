from hashlib import sha256
from typing import Union

def compute_hash(data: Union[bytes, str]) -> str:
    try:
        data = data.encode()   # https://stackoverflow.com/a/34870210
    except AttributeError:
        pass
    return sha256(data).hexdigest()