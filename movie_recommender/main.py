from pathlib import Path
import shutil

from scrape_movies import DEFAULT_GENRES, ScrapeError, scrape_movies
from suggestion import SuggestionError, format_suggestions, load_movies, suggest_by_genre

DATA_DIR = Path(__file__).parent / "data"
DATA_PATH = DATA_DIR / "movies.csv"
FALLBACK_PATH = DATA_DIR / "sample_movies.csv"


def ensure_dataset(refresh: bool = False):
    if refresh and DATA_PATH.exists():
        DATA_PATH.unlink()

    if DATA_PATH.exists():
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        print("Scraping movies... (this may take ~30 seconds)")
        scrape_movies(DEFAULT_GENRES, output_path=str(DATA_PATH))
    except ScrapeError as exc:
        # Fallback to bundled sample so the app remains usable offline.
        if FALLBACK_PATH.exists():
            shutil.copy(FALLBACK_PATH, DATA_PATH)
            print("Network scraping failed; loaded bundled sample data instead.")
        else:
            raise RuntimeError(f"Failed to scrape data and no fallback available: {exc}")


def prompt_for_genre() -> str:
    try:
        genre = input("Enter a movie genre (e.g., action, comedy, drama): ").strip()
    except (EOFError, KeyboardInterrupt):
        raise RuntimeError("Input cancelled. Please rerun the app.")
    if not genre:
        raise RuntimeError("No genre provided.")
    return genre


def main():
    try:
        ensure_dataset(refresh=False)
        genre = prompt_for_genre()

        df = load_movies(DATA_PATH)
        recommendations = suggest_by_genre(df, genre, limit=10)
        print("\nTop suggestions:")
        print(format_suggestions(recommendations.to_dict(orient="records")))
    except (RuntimeError, ScrapeError, SuggestionError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:  # Catch-all to avoid crashing the app without context.
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
