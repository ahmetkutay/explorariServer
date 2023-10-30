import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

from Configs.settings import ENCRYPTION_SALT


class EncryptionHandler:
    def __init__(self, password, salt=None):

        if salt is None:
            salt = ENCRYPTION_SALT

        self.salt = salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        print(key)
        self.cipher_suite = Fernet(key)

    def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        try:
            splitted_encrypted_data = encrypted_data.split("'")[1]
            decrypted_data = self.cipher_suite.decrypt(splitted_encrypted_data).decode()
            return decrypted_data
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None
