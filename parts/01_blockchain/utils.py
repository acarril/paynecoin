from hashlib import sha256
from typing import Union

def compute_hash(data: Union[bytes, str]) -> str:
    try:    # try to encode string to bytes
        data = data.encode()   # https://stackoverflow.com/a/34870210
    except AttributeError:  # if that fails...
        pass    # ... don't do anything
    return sha256(data).hexdigest()