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
```