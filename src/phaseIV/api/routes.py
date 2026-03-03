from fastapi import APIRouter, Request, Query, HTTPException
from pydantic import BaseModel

from phaseIV.scrapper.client import FilmNotFoundError, FilmScraperError
from phaseIV.scrapper.parser import Film

router = APIRouter()


def _client(request: Request) -> object:
    return request.app.state.client


# ---------------------------------------------------------------------------
# Film detail
# ---------------------------------------------------------------------------

@router.get(
    "/films/{film_id}",
    response_model=Film,
    summary="Get full film details",
    tags=["Films"],
)
async def get_film(film_id: int, request: Request):
    """
    Fetch the detail page for a single film by its numeric ID.

    - Served from disk cache when available (TTL: 24 h by default).
    - Raises **404** if the film does not exist on the upstream site.
    """
    try:
        return await _client(request).get_film(film_id)
    except FilmNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (FilmScraperError, ValueError) as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get(
    "/films",
    response_model=list[Film],
    summary="Get multiple films by ID",
    tags=["Films"],
)
async def get_films(
    request: Request,
    ids: list[int] = Query(..., description="Film IDs to fetch"),
    concurrency: int = Query(5, ge=1, le=20, description="Max simultaneous requests"),
):
    """
    Fetch full details for a list of film IDs concurrently.
    Results are returned in the same order as the supplied IDs.
    """
    try:
        return await _client(request).get_films(ids, concurrency=concurrency)
    except FilmNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (FilmScraperError, ValueError) as e:
        raise HTTPException(status_code=502, detail=str(e))


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class SearchResult(BaseModel):
    list_id: int | None
    films: list[Film]


@router.get(
    "/search",
    response_model=SearchResult,
    summary="Search films by title (stub info only)",
    tags=["Search"],
)
async def search_film(
    request: Request,
    title: str = Query(..., min_length=1, description="Title keyword(s) to search for"),
):
    """
    Search the library by title. Returns the upstream list ID and a list of
    films with **basic fields only** (filmID, title, year, alternative_titles).
    Use `/search/full` or `/films/{id}` to get complete details.
    """
    try:
        list_id, films = await _client(request).search_film(title)
        return SearchResult(list_id=list_id, films=films or [])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FilmScraperError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get(
    "/search/full",
    response_model=list[Film],
    summary="Search films and return full details for every result",
    tags=["Search"],
)
async def search_and_get_films(
    request: Request,
    title: str = Query(..., min_length=1, description="Title keyword(s) to search for"),
    concurrency: int = Query(5, ge=1, le=20, description="Max simultaneous detail requests"),
):
    """
    Convenience endpoint: searches by title, then fetches the full detail page
    for every result concurrently. This may take a few seconds for broad queries.
    """
    try:
        return await _client(request).search_and_get_films(title, concurrency=concurrency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FilmScraperError as e:
        raise HTTPException(status_code=502, detail=str(e))


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

@router.delete(
    "/films/{film_id}/cache",
    status_code=204,
    summary="Invalidate cached entry for one film",
    tags=["Cache"],
)
async def invalidate_film(film_id: int, request: Request):
    """Remove the cached entry for a single film, forcing a fresh fetch next time."""
    _client(request).invalidate(film_id)


@router.delete(
    "/cache",
    status_code=204,
    summary="Wipe the entire disk cache",
    tags=["Cache"],
)
async def clear_cache(request: Request):
    """Delete all cached film data."""
    _client(request).clear_cache()


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@router.get("/health", tags=["Meta"], summary="Liveness probe")
async def health():
    return {"status": "ok"}
