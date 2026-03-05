FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY src/ ./src/

RUN uv sync --no-dev --frozen

VOLUME ["/cache"]

ENV CACHE_DIR=/cache \
    CACHE_ENABLED=true \
    HTTP_TIMEOUT=10

EXPOSE 80

CMD ["uv", "run", "uvicorn", "phaseIV.api.main:app", "--host", "0.0.0.0", "--port", "80"]
