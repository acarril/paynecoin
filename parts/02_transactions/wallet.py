from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from utils import compute_hash, generate_transaction_data, convert_transaction_data_to_bytes

class Owner:
    def __init__(
        self,
        private_key,
        public_key,
        private_key_bytes,
        public_key_bytes,
        paynecoin_address
    ) -> None:
        self.private_key = private_key
        self.public_key = public_key
        self.private_key_bytes = private_key_bytes
        self.public_key_bytes = public_key_bytes
        self.paynecoin_address = paynecoin_address

def create_wallet():
    # Reference: https://stackoverflow.com/questions/2466401/how-to-generate-ssh-key-pairs-with-python
    private_key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key_bytes = private_key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    paynecoin_address = compute_hash(public_key_bytes)

    return Owner(
        private_key,
        public_key,
        private_key_bytes,
        public_key_bytes,
        paynecoin_address
    )


class Transaction:
    def __init__(
        self,
        owner: Owner,
        recipient_address,
        amount,
        signature:str=''
    ) -> None:
        self.owner = owner
        self.recipient_address = recipient_address
        self.amount = amount
        self.signature = signature
    
    def generate_data(self) -> bytes:
        transaction_data = generate_transaction_data(
            self.owner.paynecoin_address,
            self.recipient_address,
            self.amount
        )
        return convert_transaction_data_to_bytes(transaction_data)

    def sign(self):
        transaction_data = self.generate_data()
        signature = self.owner.private_key.sign(
            transaction_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.signature = signature

    def send_to_nodes(self):
        return {
            'sender_address': self.owner.paynecoin_address,
            'recipient_address': self.recipient_address,
            'amount': self.amount,
            'signature': self.signature
        }


# Test
wallet = create_wallet()
recipient_address = b'foobar'
amount = 10
transaction = Transaction(wallet, recipient_address, amount)

# verify
public_key = transaction.owner.public_key
transaction.sign()
public_key.verify(
    transaction.signature,
    transaction.generate_data(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
