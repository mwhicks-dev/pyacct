import random
import hashlib

from model.account import Password

class PasswordHash:

    @staticmethod
    def hash_password(password: str, salt: str = None) -> Password:
        if salt is None:
            salt = str(random.randrange(2 ** 24))
        
        hashed_password = hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

        return Password(salt=salt, password=hashed_password)