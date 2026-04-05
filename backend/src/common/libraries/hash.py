from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

_hasher = PasswordHasher()


def hash_value(value: str) -> str:
    return _hasher.hash(value)


def verify_hash(value: str, hashed: str) -> bool:
    try:
        return _hasher.verify(hashed, value)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False
