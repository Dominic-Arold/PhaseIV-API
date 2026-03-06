# PhaseIV API


## Development

### Test locally

Run container:
```sh
docker rm -f phaseiv-api
docker compose up -d
docker compose logs -f
```

Test in browser: http://localhost:55555/docs

Tear down, optionally deleting cache volume:
```sh
docker compose down --volumes
```# PhaseIV API

## Usage

### Docker

```shell
docker compose pull && docker compose up -d
```

## Development

### Test locally

Run container:
```sh
docker rm -f phaseiv-api
docker compose up -d
docker compose logs -f
```

Test in browser: http://localhost:55555/docs

Tear down, optionally deleting cache volume:
```sh
docker compose down --volumes
```




# Deployment

## One-time setup: PyPI Trusted Publishing

Trusted publishing uses GitHub's OIDC identity — no API tokens or secrets to rotate.
Register the repo once on both TestPyPI and PyPI.

### 1. TestPyPI (for manual testing)

1. Create an account at https://test.pypi.org
2. Go to **Account settings → Publishing → Add a new pending publisher**
3. Fill in:
   | Field | Value |
   |---|---|
   | PyPI project name | `PhaseIV-API` |
   | Owner | GitHub username |
   | Repository | `PhaseIV-API` |
   | Workflow name | `release.yml` |
   | Environment name | *(leave blank for TestPyPI)* |

### 2. PyPI (production)

1. Create an account at https://pypi.org
2. Go to **Account settings → Publishing → Add a new pending publisher**
3. Fill in the same fields as above, but set:
   | Field | Value |
   |---|---|
   | Environment name | `pypi` |

### 3. GitHub Environment

The `publish` job in `release.yml` uses `environment: pypi`.
Create this on GitHub so it matches:

1. Go to **repo → Settings → Environments → New environment**
2. Name it `pypi`
3. Optionally add required reviewers for an approval gate before every release

## Manual test deplayment

Test locally before tagging a real release.

```bash
# Tag locally so hatch-vcs resolves the version
git tag v0.1.0

# Build the package
uv build
# → dist/phaseiv_api-0.1.0-py3-none-any.whl
# → dist/phaseiv_api-0.1.0.tar.gz

# Upload to TestPyPI (configure API token once)
uvx twine upload --repository testpypi dist/*

# Optionally: Test the install from TestPyPI
#pip install \
#  --index-url https://test.pypi.org/simple/ \
#  --extra-index-url https://pypi.org/simple/ \
#  phaseiv-api==0.1.0

# Test the docker build against TestPyPI
docker build \
  --build-arg VERSION=0.1.0 \
  --build-arg PIP_INDEX_URL=https://test.pypi.org/simple/ \
  --build-arg PIP_EXTRA_INDEX_URL=https://pypi.org/simple/ \
  -t phaseiv-api:test .

docker run --rm -p 8080:80 phaseiv-api:test
# → open http://localhost:8080/docs

# Clean up local test tag before the real release
git tag -d v0.1.0
```

## Production release

```bash
git tag v0.1.0
git push origin v0.1.0
```

This triggers `release.yml`:
```
test → publish (PyPI) → [60s wait] → docker build → push to GHCR
```

The resulting image tags will be:
```
ghcr.io/<owner>/phaseiv-api:0.1.0
ghcr.io/<owner>/phaseiv-api:0.1
ghcr.io/<owner>/phaseiv-api:0
ghcr.io/<owner>/phaseiv-api:latest
```