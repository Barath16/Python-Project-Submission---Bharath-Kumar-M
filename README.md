# Movie Recommender (Scrapy + Pandas)

The Movie Recommender Bot is a Python-based application that suggests movies to users based on their preferred genre. This project demonstrates the integration of web scraping, data processing, and automation to build a functional recommendation system. The bot uses Scrapy to scrape real-time movie data from the web, processes and organizes the information with Pandas, and presents genre-specific recommendations directly to the user.

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
```bash

python main.py

```

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


movie_recommender/
│
├── README.md                 # Project documentation
├── requirements.txt          # All Python dependencies
├── scrapy.cfg                # Scrapy configuration file
│
├── moviebot/                 # Scrapy project folder
│   ├── __init__.py
│   ├── items.py              # Defines movie data fields
│   ├── pipelines.py          # Cleans/saves scraped data
│   ├── settings.py           # Scrapy settings (user-agent, delays, etc.)
│   │
│   └── spiders/
│        └── moviebot_spider.py   # Main Scrapy spider file
│
├── data/                     # Stores generated data files
│   ├── movies.csv            # Output of scraper
│
├── utils/                  
│   └── genre_filter.py       # Functions to filter movies by genre
│
├── movie_suggester.py        # Main program that interacts with the user
└── assets/                   # Images, icons, screenshots for README

