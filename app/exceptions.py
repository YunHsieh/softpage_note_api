from fastapi import HTTPException

credentials_exception = HTTPException(
    status_code=401,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

auth_verification_failure = HTTPException(
    status_code=401,
    detail='Incorrect username or password',
    headers={'x-Authenticate': 'Bearer'},
)
