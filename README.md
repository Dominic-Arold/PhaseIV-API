# PhaseIV API

[![PyPI](https://img.shields.io/pypi/v/phaseiv-api)](https://pypi.org/project/PhaseIV-API/)
[![Python](https://img.shields.io/pypi/pyversions/phaseiv-api)](https://pypi.org/project/PhaseIV-API/)
[![CI](https://github.com/dominic-arold/PhaseIV-API/actions/workflows/ci.yml/badge.svg)](https://github.com/dominic-arold/PhaseIV-API/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python async client and self-hostable REST API for the [Filmgalerie Phase IV e.V.](https://www.filmgalerie-phaseiv.de/cgi-bin/start5.pl) film lending library. Search films, fetch full metadata, and check availability — all from Python or over HTTP.

---

## Usage

### Python client

Install from PyPI:

```sh
pip install PhaseIV-API
```

**Quick one-shot calls** (no async setup needed):

```python
from phaseIV import search_film, get_film, get_films, search_and_get_films

# Search by title — returns stub results (title, year, ID)
list_id, films = search_film("The Lord of the Rings")

# Fetch full metadata for a single film by ID
film = get_film(2086)
print(film.title, film.year, film.status.available)

# Fetch multiple films concurrently
films = get_films([2086, 3351, 4341], concurrency=5)

# Search and immediately hydrate all results with full details
films = search_and_get_films("The Lord of the Rings", concurrency=5)
```

**Async client** — recommended for repeated calls or use inside async code:

```python
import asyncio
from phaseIV import PhaseivClient

async def main():
    async with PhaseivClient() as client:
        list_id, stubs = await client.search_film("The Lord of the Rings")
        films = await client.get_films(
            [f.filmID for f in stubs],
            concurrency=5,
        )
        for f in films:
            print(f.title, f.year, "✓" if f.status.available else "✗")

asyncio.run(main())
```

### REST API (Docker Compose)

Copy the [`docker-compose.yml`](docker-compose.yml) from this repo, then:

```sh
docker compose pull && docker compose up -d
```

The API is now available at **http://localhost:55555**. Interactive docs at **http://localhost:55555/docs**.

Tear down (optionally deleting the cache volume):

```sh
docker compose down --volumes
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/films/{id}` | Full metadata for one film |
| `GET` | `/films?ids=1&ids=2` | Full metadata for multiple films (concurrent) |
| `GET` | `/search?title=…` | Search by title — stub info only |
| `GET` | `/search/full?title=…` | Search and return full details for every result |
| `DELETE` | `/films/{id}/cache` | Invalidate cache for one film |
| `DELETE` | `/cache` | Wipe the entire cache |
| `GET` | `/health` | Liveness probe |

---

## Configuration

All settings can be overridden via environment variables (prefixed `PHASEIV_`) or a `.env` file.

| Variable | Default | Description |
|---|---|---|
| `PHASEIV_CACHE_ENABLED` | `true` | Enable/disable disk caching |
| `PHASEIV_CACHE_DIR` | `~/.cache/phaseIV` | Path for the disk cache |
| `PHASEIV_CACHE_TTL_HOURS` | `24.0` | Cache entry lifetime in hours |
| `PHASEIV_HTTP_TIMEOUT` | `10.0` | HTTP request timeout in seconds |

In Docker Compose, uncomment and set these under the `environment:` key:

```yaml
environment:
  PHASEIV_CACHE_ENABLED: "true"
  PHASEIV_CACHE_TTL_HOURS: "48"
  PHASEIV_HTTP_TIMEOUT: "15"
```

---

## Development

### Setup

```sh
git clone https://github.com/dominic-arold/PhaseIV-API.git
cd PhaseIV-API
uv sync --all-groups
```

### Run tests

```sh
uv run pytest
```

### Test the server locally with Docker

```sh
docker compose up -d
docker compose logs -f
```

Open **http://localhost:55555/docs** in your browser.

---

## Deployment

### Release (PyPI + GHCR)

Tag a commit to trigger the full release pipeline (`test → publish → docker build → push`):

```sh
git tag v1.2.3
git push origin v1.2.3
```

The workflow publishes to PyPI via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (no API tokens needed) and pushes the Docker image to GHCR with semver tags:

```
ghcr.io/dominic-arold/phaseiv-api:1.2.3
ghcr.io/dominic-arold/phaseiv-api:1.2
ghcr.io/dominic-arold/phaseiv-api:1
ghcr.io/dominic-arold/phaseiv-api:latest
```

### One-time PyPI Trusted Publishing setup

<details>
<summary>Expand setup instructions</summary>

#### TestPyPI

1. Create an account at https://test.pypi.org
2. Go to **Account settings → Publishing → Add a new pending publisher**
3. Fill in:

| Field | Value |
|---|---|
| PyPI project name | `PhaseIV-API` |
| Owner | GitHub username |
| Repository | `PhaseIV-API` |
| Workflow name | `release.yml` |
| Environment name | *(leave blank)* |

#### PyPI (production)

Same as above at https://pypi.org, but set **Environment name** to `pypi`.

#### GitHub Environment

1. Go to **repo → Settings → Environments → New environment**
2. Name it `pypi`
3. Optionally add required reviewers as an approval gate

</details>

### Manual test deployment

```bash
git tag v0.1.0
uv build
uvx twine upload --repository testpypi dist/*

# Test the docker build against TestPyPI
docker build \
  --build-arg VERSION=0.1.0 \
  --build-arg PIP_INDEX_URL=https://test.pypi.org/simple/ \
  --build-arg PIP_EXTRA_INDEX_URL=https://pypi.org/simple/ \
  -t phaseiv-api:test .
docker run --rm -p 8080:80 phaseiv-api:test

# Clean up
git tag -d v0.1.0
```

---

## Contributing

Bug reports and pull requests are welcome. Please open an issue first to discuss significant changes.

```sh
# Run the full test suite before submitting
uv run pytest
```

---

## License

MIT — see [LICENSE](LICENSE).
