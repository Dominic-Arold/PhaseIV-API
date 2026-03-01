import httpx
import asyncio
from bs4 import BeautifulSoup
import diskcache
from pathlib import Path
from datetime import timedelta
from phaseivAPI.scrapper.parser import parse_search_result, parse_film_information, Film


class FilmScraperError(Exception):
    """Base exception for scraper errors"""
    pass


class FilmNotFoundError(FilmScraperError):
    """Raised when a film is not found"""
    pass


class PhaseivClient:
    """Async client for scraping the film lending website"""

    BASE_URL = "https://www.filmgalerie-phaseiv.de"
    SEARCH_ENDPOINT = "/cgi-bin/suchen5.pl"
    FILM_ENDPOINT = "/cgi-bin/film5.pl"

    DEFAULT_CACHE_DIR = Path.home() / ".cache" / "phaseivAPI"
    DEFAULT_TTL = timedelta(hours=24)

    def __init__(
        self,
        timeout: float = 10.0,
        cache_dir: Path | None = None,
        cache_ttl: timedelta | None = None,
        cache_enabled: bool = True,
    ):
        self.timeout = timeout
        self.cache_enabled = cache_enabled
        self.cache_ttl = (cache_ttl or self.DEFAULT_TTL).total_seconds()

        self.client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={'User-Agent': 'Phase4API/0.1.0'}
        )

        cache_path = cache_dir or self.DEFAULT_CACHE_DIR
        self._cache = diskcache.Cache(str(cache_path)) if cache_enabled else None

        # Per-key asyncio locks to prevent redundant concurrent fetches
        self._in_flight: dict[int, asyncio.Lock] = {}
        self._in_flight_lock = asyncio.Lock() #guards _in_flight so only one coroutine creates the per-key lock

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def search_film(self, title: str) -> tuple[int | None, list[Film] | None]:
        """Search for films by title.

        Args:
            title: The film title to search for. Must be non-empty.

        Returns:
            Tuple of (list_id, films).

        Raises:
            ValueError: If title is empty.
            FilmScraperError: If the HTTP request fails.
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        url = f"{self.BASE_URL}{self.SEARCH_ENDPOINT}"
        data = {
            's': title.strip(),
            'noajax': '1'
        }

        try:
            response = await self.client.post(url, data=data)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise FilmScraperError(f"Failed to search for film: {e}") from e

        soup = BeautifulSoup(response.content, 'html.parser')
        return parse_search_result(soup)

    async def get_film(self, film_id: int) -> Film:
        """
        Get the full information for a film and return a complete Film instance.

        Args:
            film_id: The film ID

        Returns:
            A fully populated Film instance

        Raises:
            FilmNotFoundError: If the film is not found
            FilmScraperError: If the request fails
        """
        if film_id <= 0:
            raise ValueError("Film ID must be positive")

        if not self.cache_enabled:
            return await self._fetch_film(film_id)

        # 1. Check cache first (no lock needed — diskcache reads are safe)
        cached = self._cache.get(film_id)
        if cached is not None:
            return Film.model_validate_json(cached)

        # 2. Get or create a per-key lock
        async with self._in_flight_lock:
            if film_id not in self._in_flight:
                self._in_flight[film_id] = asyncio.Lock()
            key_lock = self._in_flight[film_id]

        # 3. Only one coroutine fetches; others wait, then read from cache
        async with key_lock:
            cached = self._cache.get(film_id)
            if cached is not None:
                return Film.model_validate_json(cached)
            try:
                film = await self._fetch_film(film_id)
                self._cache.set(film_id, film.model_dump_json(), expire=self.cache_ttl)
                return film
            finally:
                async with self._in_flight_lock:
                    self._in_flight.pop(film_id, None)

    async def _fetch_film(self, film_id: int) -> Film:
        """Raw HTTP fetch, no caching logic."""
        url = f"{self.BASE_URL}{self.FILM_ENDPOINT}"
        params = {'filmId': film_id}

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise FilmNotFoundError(f"Film with ID {film_id} not found") from e
            raise FilmScraperError(f"Failed to get film information: {e}") from e
        except httpx.HTTPError as e:
            raise FilmScraperError(f"Failed to get film information: {e}") from e

        soup = BeautifulSoup(response.content, 'html.parser')
        film_url = f"{url}?filmId={film_id}"
        return parse_film_information(soup, film_id=film_id, film_url=film_url)

    async def get_films(self, film_ids: list[int], concurrency: int = 5) -> list[Film]:
        """Fetch multiple films concurrently.

        Args:
            film_ids: List of film IDs to fetch.
            concurrency: Maximum number of simultaneous requests (default: 5).

        Returns:
            List of fully populated Film instances, in the same order as film_ids.
        """
        sem = asyncio.Semaphore(concurrency)

        async def fetch(fid):
            async with sem:
                return await self.get_film(fid)

        return await asyncio.gather(*[fetch(fid) for fid in film_ids])

    async def search_and_get_films(self, title: str, concurrency: int = 5) -> list[Film]:
        """Search for a title and return fully populated Film instances for all results.

        Combines search_film and get_films: first searches by title, then fetches
        the detail page for every result.

        Args:
            title: Film title to search for.
            concurrency: Maximum simultaneous detail-page requests (default: 5).

        Returns:
            List of fully populated Film instances.
        """
        _, films = await self.search_film(title)
        return await self.get_films([f.filmID for f in films], concurrency=concurrency)

    def invalidate(self, film_id: int) -> None:
        """Remove a single film from the disk cache, forcing a fresh fetch next time."""
        if self._cache:
            self._cache.delete(film_id)

    def clear_cache(self) -> None:
        """Wipe the entire disk cache."""
        if self._cache:
            self._cache.clear()


if __name__ == "__main__":

    async def main():
        async with PhaseivClient() as client:
            client.clear_cache()
            print("Searching for movie 'Soul'...")
            list_id, films = await client.search_film("Soul")
            print(films)

            film_id = 17083
            print(f"\nGetting film with ID {film_id}...")
            film = await client.get_film(film_id)
            print(film)

    asyncio.run(main())