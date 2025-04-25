from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional
from app.config import get_settings

settings = get_settings()

class EncryptionManager:
    """Handles encryption and decryption operations for sensitive data"""

    def __init__(self):
        self.salt = os.urandom(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(settings.ENCRYPTION_KEY.encode()))
        self.fernet = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypt a string using Fernet symmetric encryption"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string using Fernet symmetric encryption"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def rotate_key(self) -> None:
        """Rotate the encryption key"""
        new_key = Fernet.generate_key()
        self.fernet = Fernet(new_key)
        # Store the new key in the database
        # This would typically be done through a secure key management service

# Create a singleton instance
encryption_manager = EncryptionManager()
