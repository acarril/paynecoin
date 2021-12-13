from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from block import Block



class Node:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain

        @staticmethod
        def verify_signature(public_key, signature, transaction_data):
            public_key.verify(
                signature,
                transaction_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )