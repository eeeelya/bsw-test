import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.exceptions.http import BaseHTTPException

logger = logging.getLogger("EXCEPTION_HANDLER")


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseHTTPException)
    async def base_http_exception_handler(
        request: Request, exc: BaseHTTPException
    ) -> JSONResponse:
        logger.warning(
            f"{request.method} {request.url.path}{request.url.query}"
            f"{exc.status_code} - {exc.detail}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content={"errorMessage": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

        errors_description: list[dict[str, str]] = []
        errors = exc.errors()

        for error in errors:
            error.pop("ctx", None)
            errors_description.append(error)

        logger.warning(
            f"{request.method} {request.url.path}{request.url.query}"
            f"{status_code} - {exc.errors()}"
        )

        return JSONResponse(
            status_code=status_code, content={"errorMessage": errors_description}
        )

    @app.exception_handler(Exception)
    async def unknown_error_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

        logger.error(
            f"{request.method} {request.url.path}{request.url.query}"
            f"{status_code} - {str(exc)}"
        )

        return JSONResponse(
            status_code=status_code,
            content={"errorMessage": "Произошла непредвиденная ошибка"},
        )
