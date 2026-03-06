FROM python:3.10.17-slim

ARG VERSION

ARG PIP_INDEX_URL=https://pypi.org/simple/
ARG PIP_EXTRA_INDEX_URL
ENV PIP_INDEX_URL=${PIP_INDEX_URL}
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}

RUN pip install --no-cache-dir phaseiv-api==${VERSION}

ENV PHASEIV_CACHE_DIR=/cache

RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 80

CMD ["uvicorn", "phaseIV.api.main:app", "--host", "0.0.0.0", "--port", "80"]
