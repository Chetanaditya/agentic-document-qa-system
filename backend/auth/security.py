from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hash_password: str
) -> bool:
    """
    Verify a password against its hash
    """

    return pwd_context.verify(
        plain_password,
        hash_password
    )   