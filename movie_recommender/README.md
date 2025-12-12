# Movie Recommender (Scrape + Pandas)

A small CLI app that scrapes IMDb by genre, stores results to CSV, and serves top-rated movie suggestions for a user-provided genre. Includes a bundled sample dataset so it still works when scraping is blocked or offline.

## Features
- Scrapes IMDb search pages per genre using `requests` + `BeautifulSoup`.
- Persists results as `data/movies.csv` and reads them with `pandas`.
- CLI prompts for a genre and prints ranked suggestions (by rating, then year).
- Graceful error handling and an offline fallback dataset (`data/sample_movies.csv`).

## Prerequisites
- Python 3.9+ on PATH (`python3 --version`)
- Internet access for live scraping (optional; fallback works offline)

## Setup
```bash
cd /Users/barath/movie_recommender
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
python main.py

- On first run it tries to scrape. If blocked, it automatically copies the bundled sample CSV and still returns suggestions.
- If you want to force a fresh scrape later, delete `data/movies.csv` and run again.

## Usage Notes
- Enter genres like `action`, `comedy`, `drama`, `romance`, `thriller`, etc.
- Output is sorted by IMDb rating (desc) then year (desc).
- If no matches are found for a genre, try a simpler or broader genre string.

## Project Structure
- `main.py` – CLI entrypoint; ensures dataset, prompts genre, prints suggestions.
- `scrape_movies.py` – Scraper logic and CSV writer; defines `ScrapeError`.
- `suggestion.py` – Data loading, filtering, formatting; defines `SuggestionError`.
- `data/sample_movies.csv` – Bundled fallback dataset.
- `requirements.txt` – Dependencies.
