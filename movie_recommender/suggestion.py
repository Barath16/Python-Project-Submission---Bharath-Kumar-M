from pathlib import Path
from typing import Iterable

import pandas as pd


class SuggestionError(Exception):
    """Raised when suggestions cannot be produced."""


def load_movies(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise SuggestionError(f"Movie dataset not found at {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        raise SuggestionError(f"Could not read dataset: {exc}") from exc
    expected_columns = {"title", "year", "genres", "rating"}
    missing = expected_columns - set(df.columns)
    if missing:
        raise SuggestionError(f"Dataset missing columns: {', '.join(sorted(missing))}")
    return df


def suggest_by_genre(df: pd.DataFrame, genre: str, limit: int = 10) -> pd.DataFrame:
    if not genre:
        raise SuggestionError("Genre cannot be empty.")

    mask = df["genres"].fillna("").str.contains(genre, case=False, na=False)
    filtered = df[mask]
    if filtered.empty:
        raise SuggestionError(f"No movies found for genre '{genre}'. Try another genre.")

    # Prefer higher ratings, then recent year when rating ties.
    sorted_df = filtered.sort_values(by=["rating", "year"], ascending=[False, False])
    return sorted_df.head(limit)[["title", "year", "rating", "genres"]]


def format_suggestions(rows: Iterable[pd.Series]) -> str:
    lines = []
    for row in rows:
        title = row.get("title", "Unknown")
        year = str(row.get("year", "")).strip()
        rating = row.get("rating", "")
        genre = row.get("genres", "")
        display = f"{title} ({year})"
        if rating:
            display += f" - ⭐ {rating}"
        if genre:
            display += f" [{genre}]"
        lines.append(display)
    return "\n".join(lines)
