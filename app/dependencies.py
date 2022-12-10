import datetime

from jose import JWTError, jwt
from ormar.exceptions import NoMatch

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from app.environments import SECRET_KEY
from app.auth.models import OutstandingToken, Auth
from app.utils import datetime_to_timestamp
from app.exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='./api/login/token')


async def has_token_required(token: str = Depends(oauth2_scheme)):
    '''
    check the request that has the token or not
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY)
        if not (email := payload.get('email')):
            raise credentials_exception
        if not (exp := payload.get('exp')) and datetime_to_timestamp(exp) < datetime.datetime.utcnow():
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        await OutstandingToken.objects.get(
            token=token,
        )
    except NoMatch:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        if not (email := payload.get('email')):
            raise credentials_exception
        try:
            user = await Auth.objects.get(
                email=email
            )
        except NoMatch:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
