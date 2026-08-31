import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import settings


AccessCodeHeader = Annotated[
    str | None,
    Header(alias="X-Access-Code"),
]


def verify_access_code(
        x_access_code: AccessCodeHeader = None,
) -> None:
    """Access code for documentation Upload"""
    if x_access_code is None or not secrets.compare_digest(
        x_access_code,
        settings.access_code,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access code",
        )


def verify_query_access_code(
        x_access_code: AccessCodeHeader = None,
) -> None:
    """Access code for Query"""
    if x_access_code is None or not secrets.compare_digest(
        x_access_code,
        settings.query_access_code,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid query access code",
        )
