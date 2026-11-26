"""Print a bcrypt hash for ADMIN_PASSWORD_HASH.

Usage: python -m backend.hash_password
"""

from getpass import getpass

from .security import hash_password

if __name__ == "__main__":
    pw = getpass("Admin password: ")
    if pw != getpass("Repeat: "):
        raise SystemExit("Passwords do not match")
    if len(pw) < 12:
        raise SystemExit("Use at least 12 characters")
    print(hash_password(pw))
