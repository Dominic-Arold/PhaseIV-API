import re
from typing import Tuple

from bs4 import BeautifulSoup
from pydantic import BaseModel


class Status(BaseModel):
    """Availability and physical location of a film."""
    available: bool
    location: str


class Film(BaseModel):
    """Unified film model — required fields are populated from search results,
    optional fields are populated when fetching the detail page."""

    # Always present (parsed from search results)
    filmID: int
    title: str
    alternative_titles: list[str]
    year: int
    film_url: str

    # Populated after fetching the detail page
    image_url: str | None = None
    status: Status | None = None
    director: list[str] | None = None
    screenplay: list[str] | None = None
    main_cast: list[str] | None = None
    supporting_cast: list[str] | None = None
    cinematographer: list[str] | None = None
    composer: list[str] | None = None
    producers: list[str] | None = None
    genres: list[str] | None = None
    keywords: list[str] | None = None
    languages: list[str] | None = None
    subtitles: list[str] | None = None
    description: str | None = None


def parse_search_result(soup) -> Tuple[int | None, list[Film] | None]:
    """Parse the search result page and return (list_id, films).

    Locates the 'Filme' section in the HTML and extracts all film entries
    found within it.

    Args:
        soup: Parsed BeautifulSoup object of the search results page.

    Returns:
        Tuple of (list_id, films) where list_id is a int identifier
        for the result list and films is a list of Film instances.
        If parsing fails, returns (None, None).
    """
    films = []
    list_id = None
    mainmatter = soup.find('div', id='mainmatter')

    # Find the "Filme" section
    film_section = None
    for h4 in mainmatter.find_all('h4'):
        if h4.get_text(strip=True) == 'Filme':
            film_section = h4
            break
    if film_section is None:
        return None, None
    # Collect all film entries (p.filmshort) until the next h4
    current = film_section.find_next_sibling()
    while current and current.name != 'h4':
        if current.name == 'p' and 'filmshort' in current.get('class', []):
            list_id, film_data = parse_search_result_entry(current)
            if film_data:
                films.append(film_data)
        current = current.find_next_sibling()

    return list_id, films


def parse_search_result_entry(p_tag) -> Tuple[int | None, Film | None]:
    """Parse a single film entry (<p class='filmshort'>) from a search result page.

    Extracts the film ID, list ID, image URL, title, year, and alternative
    titles from the anchor tag and surrounding text.

    Args:
        p_tag: A BeautifulSoup Tag representing a single search result entry.

    Returns:
        Tuple of (list_id, Film). Returns (None, None) if no anchor tag is found.
    """
    a_tag = p_tag.find('a')
    if not a_tag:
        return None, None

    href = a_tag.get('href', '')
    film_id = None
    list_id = None

    if 'filmId=' in href:
        m = re.search(r'filmId=(\d+)', href)
        if m:
            film_id = int(m.group(1))

    if 'listId=' in href:
        m = re.search(r'listId=(\d+)', href)
        if m:
            list_id = m.group(1)
    # ignore image url in search result. Inconsistent urls when parsing from search and film page
    # ("...images/filme..." vs "...images//filme..."). Parse image_url only from film page, since it is a detail.
    # Image URL from onmouseover
    #image_url = None
    #onmouseover = a_tag.get('onmouseover', '')
    #if onmouseover:
    #    m = re.search(r"change_mouse\('([^']+)'\)", onmouseover)
    #    if m:
    #        image_url = m.group(1)

    title = a_tag.get_text(strip=True)
    full_text = p_tag.get_text()
    text_after_title = full_text.replace(title, '', 1).strip()

    # Year (4 digits at end)
    year = None
    year_match = re.search(r'\b(\d{4})\s*$', text_after_title)
    if year_match:
        year = int(year_match.group(1))
        text_after_title = text_after_title[:year_match.start()].strip()

    # Alternative titles in parentheses
    alt_titles = [alt.strip() for alt in re.findall(r'\(([^)]+)\)', text_after_title)]

    return int(list_id), Film(
        filmID=film_id,
        title=title,
        alternative_titles=alt_titles,
        year=year,
        film_url=href,
    )


def parse_film_information(soup: BeautifulSoup, film_id: int, film_url: str) -> Film:
    """
    Parse the film detail page and return a complete Film instance.

    Args:
        soup:       Parsed HTML of the detail page.
        film_id:    The film ID (from the request URL, not available in page body).
        film_url: The canonical URL used to fetch this page.

    Returns:
        A fully populated Film instance.
    """

    # ------------------------------------------------------------------ #
    # Header block: title, alternative titles, year, image                #
    # ------------------------------------------------------------------ #
    title = ""
    title_span = soup.find('span', class_='filmtitel')
    if title_span:
        title = title_span.get_text(strip=True)

    # The <p> containing the title span also holds alt-titles and year:
    # <span class='filmtitel'>…</span><br>(AltA / AltB)<br> … 1973 …
    alternative_titles: list[str] = []
    year: int | None = None

    title_p = title_span.find_parent('p') if title_span else None
    if title_p:
        raw = title_p.get_text(separator=' ')
        # Remove main title
        raw = raw.replace(title, '', 1).strip()

        # Year
        year_match = re.search(r'\b(\d{4})\b', raw)
        if year_match:
            year = int(year_match.group(1))

        # Alt titles inside parentheses — may be slash-separated
        for group in re.findall(r'\(([^)]+)\)', raw):
            for part in group.split('/'):
                part = part.strip()
                if part:
                    alternative_titles.append(part)

    # Cover image (first img inside the first p.smallskip)
    image_url = ""
    first_smallskip = soup.find('p', class_='smallskip')
    if first_smallskip:
        img = first_smallskip.find('img')
        if img:
            image_url = img.get('src', '')
            # image_url from film page is inconsistent with url from search result page

    # ------------------------------------------------------------------ #
    # Table rows                                                           #
    # ------------------------------------------------------------------ #
    FIELD_MAP = {
        'Genre':      'genres',
        'Stichwort':  'keywords',
        'Sprachen':   'languages',
        'Untertitel': 'subtitles',
        'Hauptrolle': 'main_cast',
        'Nebenrolle': 'supporting_cast',
        'Produzent':  'producers',
        'Regie':      'director',
        'Drehbuch':   'screenplay',
        'Kamera':     'cinematographer',
        'Musik':      'composer',
    }

    status_available: bool | None = None
    status_location: str | None = None
    field_values: dict[str, list[str]] = {}

    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue

        label = cells[0].get_text(strip=True)
        value_cell = cells[1]
        value_text = value_cell.get_text(strip=True)

        if label == 'Status':
            lower = value_text.lower()
            if 'verf' in lower:          # verfügbar (may be HTML-encoded)
                status_available = True
            elif 'ausgeliehen' in lower:
                status_available = False
            # else: unknown — leave None

        elif label == 'Standort':
            status_location = value_text

        elif label in FIELD_MAP:
            links = value_cell.find_all('a')
            if links:
                field_values[FIELD_MAP[label]] = [
                    a.get_text(strip=True).replace('\xa0', ' ') for a in links
                ]
            elif value_text:
                field_values[FIELD_MAP[label]] = [value_text.replace('\xa0', ' ')]

    # ------------------------------------------------------------------ #
    # Description (first two p.smallskip, text + inline links only)       #
    # ------------------------------------------------------------------ #
    description: str | None = None
    desc_paragraphs = soup.find_all('p', class_='smallskip')
    if desc_paragraphs:
        parts: list[str] = []
        for p in desc_paragraphs[:2]:
            seg: list[str] = []
            for node in p.children:
                if isinstance(node, str):
                    text = node.strip()
                    if text:
                        seg.append(text)
                elif node.name == 'a':
                    text = node.get_text(strip=True).replace('\xa0', ' ')
                    if text:
                        seg.append(text)
                # skip img, ul, etc.
            if seg:
                parts.append(' '.join(seg))
        description = ' '.join(parts) if parts else None

    # ------------------------------------------------------------------ #
    # Assemble and return                                                  #
    # ------------------------------------------------------------------ #
    status: Status | None = None
    if status_available is not None and status_location is not None:
        status = Status(available=status_available, location=status_location)

    return Film(
        filmID=film_id,
        title=title,
        alternative_titles=alternative_titles,
        year=year,
        image_url=image_url,
        film_url=film_url,
        status=status,
        description=description,
        **field_values,
    )