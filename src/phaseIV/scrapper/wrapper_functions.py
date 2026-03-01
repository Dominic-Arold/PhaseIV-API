import asyncio
from phaseivAPI.scrapper.client import PhaseivClient
from phaseivAPI.scrapper.parser import Film

def _run(coro_fn, **client_kwargs):
    async def _inner():
        async with PhaseivClient(**client_kwargs) as client:
            return await coro_fn(client)
    return asyncio.run(_inner())

def search_film(title: str, **client_kwargs) -> tuple[str, list[Film]]:
    """
    One-shot convenience wrapper around PhaseivClient.search_film.
    Spins up a temporary client, runs the coroutine, and returns the result.
    For repeated calls, use PhaseivClient directly to share the connection and utilize concurrency.
    """
    return _run(lambda c: c.search_film(title), **client_kwargs)

def get_film(film_id: int, **client_kwargs) -> Film:
    """
    One-shot convenience wrapper around PhaseivClient.get_film.
    Spins up a temporary client, runs the coroutine, and returns the result.
    For repeated calls, use PhaseivClient directly to share the connection and utilize concurrency.
    """
    return _run(lambda c: c.get_film(film_id), **client_kwargs)

def get_films(film_ids: list[int], concurrency: int = 5, **client_kwargs) -> list[Film]:
    """
    One-shot convenience wrapper around PhaseivClient.get_films.
    Spins up a temporary client, runs the coroutine, and returns the result.
    """
    return _run(lambda c: c.get_films(film_ids, concurrency), **client_kwargs)

def search_and_get_films(title: str, concurrency: int = 5, **client_kwargs) -> list[Film]:
    """
    One-shot convenience wrapper around PhaseivClient.search_and_get_films.
    Spins up a temporary client, runs the coroutine, and returns the result.
    """
    return _run(lambda c: c.search_and_get_films(title, concurrency), **client_kwargs)