import typing
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import settings

get_bearer_token = HTTPBearer(auto_error=False)


def auth_middleware(token: str = settings.ADMIN_TOKEN) -> typing.Callable:
    async def authorize_token(auth: typing.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)) -> str:
        """
        Authorizes the token for the routes requiring admin access.
        :param auth: The HTTP authorization credentials.
        :return: The token.
        """
        nonlocal token
        if auth is None or (incoming_token := auth.credentials) != token:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )
        return incoming_token
    return authorize_token
