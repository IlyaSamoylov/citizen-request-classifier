from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import (
	BaseAppException,
    RequestNotFoundError,
    ClarificationNotFoundError,
    ClarificationAlreadyAnsweredError,
    ClassificationFailedError,
    PersistenceError,
)


async def app_error_handler(request: Request, exc: BaseAppException):
    if isinstance(exc, (RequestNotFoundError, ClarificationNotFoundError)):
        status_code = 404
    elif isinstance(exc, ClarificationAlreadyAnsweredError):
        status_code = 409
    elif isinstance(exc, ClassificationFailedError):
        status_code = 422
    elif isinstance(exc, PersistenceError):
        status_code = 500
    else:
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )