import hashlib
import bcrypt

# Hashing with bcrypt
def hash_bcrypt(password: str) -> bytes:
    """Hashing the password with bcrypt with random salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# For verifying the user's password hash against stored hash
def verify_bcrypt(password: str, stored_hash: bytes) -> bool:
    """Verify password against stored bcrypt hash"""
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)