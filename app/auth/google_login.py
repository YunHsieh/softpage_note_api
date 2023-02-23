import requests

from jose import jwt
from urllib.parse import urljoin
from fastapi import APIRouter, HTTPException, Request
from app.auth.base_models import Token
from app.auth.models import Auth
from app.auth.login import create_access_token
from fastapi.responses import RedirectResponse
from app.stores import database
from app.environments import (
    CLIENT_HOST,
    GOOGLE_OAUTH_URL,
    GOOGLE_TOKEN_URL,
    GOOGLE_OAUTH_SCOPE,
    CLIENT_ID,
    CLIENT_SECRET,
)

router = APIRouter(
    prefix='/api/google',
    tags=['login', 'auth'],
    responses={404: {'description': 'Not found'}},
)

REDIRECT_URI = 'oauth2callback'


@router.get('/authorize', response_model=Token)
async def oauth2callback(request: Request):
    req_args = dict(request.query_params)
    payload = {
        'client_id': CLIENT_ID,
        'redirect_uri': urljoin(request.url._url, router.url_path_for(REDIRECT_URI)),
    }
    if 'code' not in req_args:
        params = payload | {
            'response_type': 'code',
            'scope': GOOGLE_OAUTH_SCOPE,
        }
        return {
            'redirect_url': f'{GOOGLE_OAUTH_URL}?{"&".join(f"{k}={v}" for k, v in params.items())}'
        }
    else:
        auth_code = req_args.get('code')
        data = payload | {
            'code': auth_code,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code'
        }
        r = requests.post(GOOGLE_TOKEN_URL, data=data)
        user_profile = jwt.get_unverified_claims(r.json()['id_token'])
        # TODO: the client host could be bring from the client.
        return RedirectResponse(
            urljoin(CLIENT_HOST, 'auth') + f'?access_token={await user_info(user_profile)}'
        )


async def user_info(info: dict):
    if not info.get('email'):
        return HTTPException(400)
    user = await Auth.objects.get_or_none(email=info.get('email'))
    if not user:
        user = await Auth(
            email=info.get('email', ''),
            username=info.get('name', ''),
            password="",
            avatar=info.get('picture', ''),
            email_verified=True,
        ).save()
    return await create_access_token(user, extra_info={
        'issuer': info.get('iss', '') 
    })
