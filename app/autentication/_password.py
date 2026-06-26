import bcrypt

from app.core.domain_exception import DomainException

_BCRYPT_MAX_BYTES = 72


def _fits_bcrypt(password: str) -> bool:
    return len(password.encode("utf-8")) <= _BCRYPT_MAX_BYTES


def get_password_hash(password: str) -> str:
    DomainException.validate(
        _fits_bcrypt(password),
        "Password must be at most 72 bytes in UTF-8 for bcrypt compatibility.",
    )
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not _fits_bcrypt(plain):
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))