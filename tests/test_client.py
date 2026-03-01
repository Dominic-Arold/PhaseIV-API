"""Unit tests for PhaseivClient."""

import pytest
from bs4 import BeautifulSoup

from phaseIV.scrapper.client import PhaseivClient, FilmScraperError, FilmNotFoundError
from phaseIV.scrapper.parser import Film, parse_search_result, parse_film_information


def make_response(content: str, status_code: int = 200):
    """Build a minimal mock httpx.Response using a plain object."""
    import httpx

    class _FakeRequest:
        url = "http://fake"

    class _FakeResponse:
        def __init__(self):
            self.status_code = status_code
            self.content = content.encode("utf-8")

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    message=f"HTTP {self.status_code}",
                    request=_FakeRequest(),
                    response=self,
                )

    return _FakeResponse()


# ---------------------------------------------------------------------------
# Parser tests (pure, no I/O)
# ---------------------------------------------------------------------------

class TestParseSearchResult:
    def test_returns_list_id_and_films(self, search_html, search_list_id, search_num_results):
        soup = BeautifulSoup(search_html, "html.parser")
        list_id, films = parse_search_result(soup)

        assert list_id == search_list_id
        assert len(films) == search_num_results

    def test_film_fields(self, search_html, film):
        soup = BeautifulSoup(search_html, "html.parser")
        _, films = parse_search_result(soup)
        film = films[0]

        assert film.filmID == film.filmID
        assert film.title == film.title
        assert film.year == film.year
        assert film.alternative_titles == film.alternative_titles


class TestParseFilmInformation:
    def test_full_film(self, film_html, film):
        soup = BeautifulSoup(film_html, "html.parser")
        film_result = parse_film_information(soup, film_id=film.filmID, film_url=film.film_url)

        assert film_result.filmID == film.filmID
        assert film_result.title == film.title
        assert film_result.alternative_titles == film.alternative_titles
        assert film_result.year == film.year
        assert film_result.image_url == film.image_url
        assert film_result.film_url == film.film_url
        assert film_result.status.available == film.status.available
        assert film_result.status.location == film.status.location
        assert film_result.director == film.director
        assert film_result.screenplay == film.screenplay
        assert film_result.main_cast == film.main_cast
        assert film_result.supporting_cast == film.supporting_cast
        assert film_result.cinematographer == film.cinematographer
        assert film_result.composer == film.composer
        assert film_result.producers == film.producers
        assert film_result.genres == film.genres
        assert film_result.keywords == film.keywords
        assert film_result.languages == film.languages
        assert film_result.subtitles == film.subtitles
        assert film_result.description == film.description


# ---------------------------------------------------------------------------
# PhaseivClient async tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSearchFilm:
    async def test_returns_films(
            self, no_cache_client, mocker, search_title, search_html, search_list_id, search_num_results
    ):
        mocker.patch.object(
            no_cache_client.client, "post", new_callable=mocker.AsyncMock, return_value=make_response(search_html)
        )
        list_id, films = await no_cache_client.search_film(search_title)

        assert list_id == search_list_id
        assert len(films) == search_num_results

    async def test_empty_title_raises(self, no_cache_client):
        with pytest.raises(ValueError, match="empty"):
            await no_cache_client.search_film("   ")

    async def test_http_error_raises_scraper_error(self, no_cache_client, mocker, search_title):
        import httpx
        mocker.patch.object(
            no_cache_client.client, "post", new_callable=mocker.AsyncMock,
            side_effect=httpx.HTTPError("connection failed")
        )
        with pytest.raises(FilmScraperError):
            await no_cache_client.search_film(search_title)

    async def test_post_called_with_correct_params(self, no_cache_client, mocker, search_title, search_html):
        mock_post = mocker.patch.object(no_cache_client.client, "post", new_callable=mocker.AsyncMock,
                                        return_value=make_response(search_html))
        await no_cache_client.search_film(search_title)

        _, kwargs = mock_post.call_args
        assert kwargs["data"]["s"] == search_title
        assert kwargs["data"]["noajax"] == "1"


@pytest.mark.asyncio
class TestGetFilm:
    async def test_returns_film(self, no_cache_client, mocker, film_html, film):
        mocker.patch.object(no_cache_client.client, "get", new_callable=mocker.AsyncMock,
                            return_value=make_response(film_html))
        film_result = await no_cache_client.get_film(film.filmID)

        assert film_result.filmID == film.filmID
        assert film_result.title == film.title

    async def test_invalid_id_raises(self, no_cache_client):
        with pytest.raises(ValueError):
            await no_cache_client.get_film(0)

    async def test_404_raises_film_not_found(self, no_cache_client, mocker, film):
        mocker.patch.object(
            no_cache_client.client, "get", new_callable=mocker.AsyncMock,
            return_value=make_response("", status_code=404)
        )
        with pytest.raises(FilmNotFoundError):
            await no_cache_client.get_film(film.filmID)

    async def test_500_raises_scraper_error(self, no_cache_client, mocker, film):
        mocker.patch.object(
            no_cache_client.client, "get", new_callable=mocker.AsyncMock,
            return_value=make_response("", status_code=500)
        )
        with pytest.raises(FilmScraperError):
            await no_cache_client.get_film(film.filmID)


@pytest.mark.asyncio
class TestGetFilms:
    async def test_fetches_all_films(self, no_cache_client, mocker):
        mocker.patch.object(
            no_cache_client, "get_film", new_callable=mocker.AsyncMock,
                side_effect=lambda fid: Film(
                    filmID=fid, title=f"Film {fid}",
                    alternative_titles=[], year=2000, film_url="",
                )
        )
        films = await no_cache_client.get_films([1, 2, 3])

        assert len(films) == 3
        assert {f.filmID for f in films} == {1, 2, 3}

    async def test_preserves_order(self, no_cache_client, mocker):
        ids = [10, 20, 30]
        mocker.patch.object(
            no_cache_client, "get_film", new_callable=mocker.AsyncMock,
                side_effect=lambda fid: Film(
                    filmID=fid, title=f"Film {fid}",
                    alternative_titles=[], year=2000, film_url="",
                )
        )
        films = await no_cache_client.get_films(ids)

        assert [f.filmID for f in films] == ids

    async def test_empty_list_returns_empty(self, no_cache_client):
        films = await no_cache_client.get_films([])
        assert films == []


@pytest.mark.asyncio
class TestSearchAndGetFilms:
    async def test_combines_search_and_fetch(self, no_cache_client, mocker, film):
        stub_films = [
            Film(filmID=film.filmID, title=film.title, alternative_titles=film.alternative_titles,
                 year=film.year, film_url=film.film_url),
            Film(filmID=film.filmID + 1, title=film.title + " 2", alternative_titles=[],
                 year=film.year + 1, film_url=film.film_url),
        ]
        mock_search = mocker.patch.object(
            no_cache_client, "search_film", new_callable=mocker.AsyncMock,
            return_value=(287, stub_films)
        )
        mock_get_films = mocker.patch.object(
            no_cache_client, "get_films", new_callable=mocker.AsyncMock,
            return_value=stub_films
        )

        result = await no_cache_client.search_and_get_films(film.title)

        mock_search.assert_called_once_with(film.title)
        mock_get_films.assert_called_once_with([stub_films[0].filmID, stub_films[1].filmID], concurrency=5)
        assert result == stub_films


# ---------------------------------------------------------------------------
# Caching tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestCaching:
    async def test_cache_hit_skips_http(self, tmp_path, mocker, film):
        client = PhaseivClient(cache_dir=tmp_path, cache_enabled=True)
        client._cache.set(film.filmID, film.model_dump_json())

        mock_fetch = mocker.patch.object(client, "_fetch_film", new_callable=mocker.AsyncMock)
        result = await client.get_film(film.filmID)

        mock_fetch.assert_not_called()
        assert result.filmID == film.filmID
        assert result.title == film.title
        await client.close()

    async def test_cache_miss_calls_http_and_stores(self, tmp_path, mocker, film):
        client = PhaseivClient(cache_dir=tmp_path, cache_enabled=True)

        mocker.patch.object(client, "_fetch_film", new_callable=mocker.AsyncMock, return_value=film)
        result = await client.get_film(film.filmID)

        assert result.title == film.title
        assert client._cache.get(film.filmID) is not None
        await client.close()

    async def test_invalidate_removes_entry(self, tmp_path, film):
        client = PhaseivClient(cache_dir=tmp_path, cache_enabled=True)
        client._cache.set(film.filmID, film.model_dump_json())
        client.invalidate(film.filmID)

        assert client._cache.get(film.filmID) is None
        await client.close()

    async def test_clear_cache_wipes_all(self, tmp_path, film):
        client = PhaseivClient(cache_dir=tmp_path, cache_enabled=True)
        for i, fid in enumerate([film.filmID, film.filmID + 1, film.filmID + 2]):
            f = film.model_copy(update={"filmID": fid, "title": f"Film {i}"})
            client._cache.set(fid, f.model_dump_json())

        client.clear_cache()

        for fid in [film.filmID, film.filmID + 1, film.filmID + 2]:
            assert client._cache.get(fid) is None
        await client.close()