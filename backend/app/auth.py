import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import settings


def verify_access_code(
        x_access_code: Annotated[
            str | None, Header(alias="X-Access-Code"),
        ] = None
) -> None:
    if x_access_code is None or not secrets.compare_digest(
        x_access_code,
        settings.access_code,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access code",
        )