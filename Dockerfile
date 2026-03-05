FROM python:3.10.17-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files and README before installing so that changes to src/
# do not bust the uv sync cache layer.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --no-dev --frozen --no-cache

COPY src/ ./src/

# Run as a non-root user to limit blast radius if the app is compromised.
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 80

CMD ["uv", "run", "uvicorn", "phaseIV.api.main:app", "--host", "0.0.0.0", "--port", "80"]