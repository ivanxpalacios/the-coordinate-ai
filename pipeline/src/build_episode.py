import csv
import json
import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator

RAW_CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "episodes_raw.csv"
OUTPUT_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "episodes.json"


class Episode(BaseModel):
    global_number: int
    season: int
    episode_in_season: int
    title: str
    wiki_title: str | None = None
    arc: str
    manga_chapters: list[int]

    @field_validator("manga_chapters", mode="before")
    @classmethod
    def split_manga_chapters(cls, value: str) -> list[str]:
        return value.split("|")

    @field_validator("wiki_title", mode="before")
    @classmethod
    def blank_wiki_title_to_none(cls, value: str | None) -> str | None:
        return value or None


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_episodes(rows: list[dict[str, str]]) -> tuple[list[Episode], list[str]]:
    episodes: list[Episode] = []
    errors: list[str] = []
    for line_number, row in enumerate(rows, start=2):
        try:
            episodes.append(Episode(**row))
        except ValidationError as e:
            errors.append(f"Fila {line_number}: {e}")
    return episodes, errors


def check_global_number_invariants(episodes: list[Episode]) -> list[str]:
    errors: list[str] = []
    numbers = [ep.global_number for ep in episodes]

    seen: set[int] = set()
    duplicates: set[int] = set()
    for n in numbers:
        if n in seen:
            duplicates.add(n)
        seen.add(n)
    if duplicates:
        errors.append(f"global_number duplicados: {sorted(duplicates)}")

    expected = set(range(1, len(episodes) + 1))
    missing = expected - seen
    if missing:
        errors.append(f"global_number faltantes en la secuencia: {sorted(missing)}")

    return errors


def main() -> None:
    rows = load_rows(RAW_CSV_PATH)
    episodes, errors = build_episodes(rows)
    errors.extend(check_global_number_invariants(episodes))

    if errors:
        print("Se encontraron errores, no se escribió episodes.json:\n")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    OUTPUT_JSON_PATH.write_text(
        json.dumps([ep.model_dump() for ep in episodes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"{len(episodes)} episodios escritos en {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
