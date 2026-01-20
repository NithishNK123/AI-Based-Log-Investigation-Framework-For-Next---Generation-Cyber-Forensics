"""
encrypt.py
----------
Handles encryption of log data before sending it to the server.

Uses symmetric encryption (Fernet - AES based).
The encryption key is generated once and stored locally.
"""

from cryptography.fernet import Fernet
import os

# File where encryption key is stored
KEY_FILE = ".agent_secret.key"


def generate_key():
    """
    Generate a new encryption key and save it locally.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """
    Load encryption key from local storage or generate one if not present.

    Returns:
        bytes: Encryption key
    """
    if not os.path.exists(KEY_FILE):
        return generate_key()

    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


def encrypt(data: bytes) -> bytes:
    """
    Encrypt data using Fernet symmetric encryption.

    Args:
        data (bytes): Raw data to encrypt

    Returns:
        bytes: Encrypted data
    """
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt(encrypted_data: bytes) -> bytes:
    """
    Decrypt data using Fernet symmetric encryption.

    Args:
        encrypted_data (bytes): Encrypted data

    Returns:
        bytes: Decrypted data
    """
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)