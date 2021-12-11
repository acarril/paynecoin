from datetime import datetime, timezone
import json

from paynecoin.nodes.utils import compute_hash

class Block:
    def __init__(self,
            transaction_data:dict,
            previous_block=None,
            timestamp:str=None
        ) -> None:
        self.transaction_data = transaction_data
        self.previous_block = previous_block
        self.timestamp = timestamp if timestamp else str(datetime.now(timezone.utc))

    @property
    def previous_block_hash(self):
        previous_block_hash = self.previous_block.hash if self.previous_block else ''
        return previous_block_hash

    @property
    def hash(self) -> str:
        block_content = {
            'transaction_data': self.transaction_data,
            'previous_block_hash': self.previous_block_hash,
            'timestamp': self.timestamp
        }
        block_content_bytes = json.dumps(block_content, indent=2).encode('utf-8')
        return compute_hash(block_content_bytes)