import os
import time
from typing import Iterable, List, Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup

IMDB_SEARCH_URL = "https://www.imdb.com/search/title/"
DEFAULT_GENRES = ["action", "adventure", "animation", "comedy", "drama", "horror", "romance", "sci-fi", "thriller"]


class ScrapeError(Exception):
    """Raised when scraping fails for all provided genres."""


def _get_headers() -> Dict[str, str]:
    # A lightweight user agent helps avoid basic blocking from IMDb.
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }


def _fetch_genre_page(genre: str, count: int) -> str:
    params = {
        "genres": genre,
        "title_type": "feature",
        "sort": "user_rating,desc",
        "count": str(count),
    }
    response = requests.get(IMDB_SEARCH_URL, params=params, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    return response.text


def _parse_movies(html: str, genre: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    movies = []
    for item in soup.select("div.lister-item"):
        title_tag = item.select_one("h3.lister-item-header a")
        year_tag = item.select_one("span.lister-item-year")
        genre_tag = item.select_one("span.genre")
        rating_tag = item.select_one("div.inline-block.ratings-imdb-rating strong")

        if not title_tag:
            continue

        title = title_tag.text.strip()
        year_text = year_tag.text.strip() if year_tag else ""
        # Extract the last 4 consecutive digits as the year when possible.
        year = ""
        for token in year_text.split():
            if token.strip("()").isdigit() and len(token.strip("()")) == 4:
                year = token.strip("()")
        genres = genre_tag.text.strip().replace("\n", "").replace(" ", "") if genre_tag else genre
        rating = rating_tag.text.strip() if rating_tag else ""

        movies.append(
            {
                "title": title,
                "year": year,
                "genres": genres.lower(),
                "rating": float(rating) if rating.replace(".", "", 1).isdigit() else None,
                "source_genre": genre.lower(),
            }
        )
    return movies


def scrape_movies(
    genres: Iterable[str] = DEFAULT_GENRES,
    output_path: str = "data/movies.csv",
    per_genre: int = 30,
    delay_seconds: float = 0.5,
) -> pd.DataFrame:
    """
    Scrape IMDb for multiple genres and persist results to CSV.

    Returns the collected DataFrame. Raises ScrapeError if all genres fail.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    collected: List[Dict[str, str]] = []
    failed: List[str] = []

    for genre in genres:
        try:
            html = _fetch_genre_page(genre, count=per_genre)
            parsed = _parse_movies(html, genre)
            if not parsed:
                failed.append(genre)
                continue
            collected.extend(parsed)
            time.sleep(delay_seconds)
        except (requests.RequestException, Exception):
            failed.append(genre)
            continue

    if not collected:
        raise ScrapeError(f"Could not scrape data for any genres: {', '.join(failed)}")

    df = pd.DataFrame(collected).drop_duplicates(subset=["title", "year"], keep="first")
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    # Manual run helper
    try:
        data = scrape_movies()
        print(f"Scraped {len(data)} movies into data/movies.csv")
    except ScrapeError as exc:
        print(f"Scrape failed: {exc}")
