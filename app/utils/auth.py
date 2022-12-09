from passlib.hash import pbkdf2_sha256
from app.environments import SECRET_KEY


def make_password(password):
    return pbkdf2_sha256.hash(f'{password}{SECRET_KEY}')


def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(f'{password}{SECRET_KEY}', hashed_password)