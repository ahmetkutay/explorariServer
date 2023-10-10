from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import os


class EncryptionHandler:
    def __init__(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)  # Generate a random salt if not provided

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # You can adjust the number of iterations for more security
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher_suite = Fernet(key)

    def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data
