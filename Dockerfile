FROM python:3.10.17-slim

ARG VERSION

# PIP_INDEX_URL and PIP_EXTRA_INDEX_URL are standard pip env vars, read automatically.
# Defaults point to real PyPI. Override for local testing against TestPyPI:
#   docker build \
#     --build-arg VERSION=0.1.0 \
#     --build-arg PIP_INDEX_URL=https://test.pypi.org/simple/ \
#     --build-arg PIP_EXTRA_INDEX_URL=https://pypi.org/simple/ \
#     -t phaseiv-api:test .
ARG PIP_INDEX_URL=https://pypi.org/simple/
ARG PIP_EXTRA_INDEX_URL
ENV PIP_INDEX_URL=${PIP_INDEX_URL}
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}

RUN pip install --no-cache-dir phaseiv-api==${VERSION}

# Run as a non-root user to limit blast radius if the app is compromised.
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 80

CMD ["uvicorn", "phaseIV.api.main:app", "--host", "0.0.0.0", "--port", "80"]
