import datetime
import random

from jose import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ormar.exceptions import NoMatch

from app.auth.base_models import Token
from app.environments import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.models import Auth, OutstandingToken
from app.stores import database
from app.utils import get_millisecond_timestamp, verify_password
from app.exceptions import auth_verification_failure

router = APIRouter(
    prefix='/login',
    tags=['items'],
    responses={404: {'description': 'Not found'}},
)


async def authenticate_user(email: str, password: str) -> Auth:
    try:
        user = await Auth.objects.get(email=email)
    except NoMatch as _:
        raise auth_verification_failure
    if all([
        not user,
        not verify_password(password, user.password),
    ]):
        return False
    return user


async def create_access_token(user: Auth, expires_delta: datetime.timedelta | None = None):
    current_time = datetime.datetime.utcnow()
    # TODO: add cache
    queryset = await OutstandingToken.objects.filter(
        user=user,
        expires_at__gte=current_time
    ).order_by('expires_at').all()
    if queryset:
        return queryset[0].token

    to_encode = {
        'username': user.username,
        'email': user.email,
        'iat': get_millisecond_timestamp(current_time)
    }
    if not expires_delta:
        expires_delta = datetime.timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode |= {'exp': get_millisecond_timestamp(current_time + expires_delta)}
    datetime_str = current_time.strftime('%y%m%d')
    # write a new jwt record
    await OutstandingToken(
        user=user,
        jti=f'id:{datetime_str}{random.randint(1,99999):05}',
        token=jwt.encode(to_encode, SECRET_KEY),
        expires_at=current_time + expires_delta,
    ).save()
    return jwt.encode(to_encode, SECRET_KEY)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    OAuth2PasswordRequestForm: fastapi docs register interface
    '''
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise auth_verification_failure

    access_token_expires = datetime.timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token(
        user=user, expires_delta=access_token_expires
    )
    return {
        'access_token': access_token, 
        'token_type': 'bearer',
    }
