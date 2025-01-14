FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2

RUN apk --no-cache add python3-dev zlib-dev libc-dev gcc

WORKDIR /app

COPY ./app /app/
COPY ./pyproject.toml ./poetry.lock /app/

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--loop", "uvloop", "--reload"]
