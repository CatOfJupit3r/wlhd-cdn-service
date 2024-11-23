import typing
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import settings

get_bearer_token = HTTPBearer(auto_error=False)


async def authorize_token(auth: typing.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)) -> str:
    """
    Authorizes the token for the routes requiring admin access.
    :param auth: The HTTP authorization credentials.
    :return: The token.
    """
    if auth is None or (token := auth.credentials) != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token",
        )
    return token
