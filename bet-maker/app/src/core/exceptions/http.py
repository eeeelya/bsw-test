from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Непредвиденная ошибка"

    def __init__(
        self, status_code: int | None = None, detail: str | None = None
    ) -> None:
        self.status_code: int = status_code or self.status_code
        self.detail: str = detail or self.detail

        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFound(BaseHTTPException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Объект не найден"


class BadRequest(BaseHTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Неправильный запрос"
