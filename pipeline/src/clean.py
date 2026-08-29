"""Cleans raw wikitext and converts it into structured plain text.

Removes templates ({{...}}), references (<ref>...</ref>), HTML tags,
comments, and link/bolding markup, leaving behind prose suitable
for chunking.

Known limitation: only the templates listed in CONTENT_TEMPLATE_ARG
(nihongo, w) retain their visible text before the remaining
templates are completely removed. If another template containing
prose (rather than a structured field like an Infobox) appears,
it must be added to that list; otherwise, its content is lost.
For this spike, this is acceptable because the manual review
(Phase 5, step 3 of PROJECT.md) audits the result.
"""

import re
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
REF_PATTERN = re.compile(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", re.DOTALL)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
LINK_PATTERN = re.compile(r"\[\[([^\]|]*\|)?([^\]]+)\]\]")
FILE_LINK_PATTERN = re.compile(r"\[\[\s*(?:File|Image):[^\]]*\]\]", re.IGNORECASE)
BOLD_ITALIC_PATTERN = re.compile(r"'{2,5}")

# Templates where the visible text is in a positional argument, not in a
# structured field (unlike {{Infobox episode | Season = 1 | ...}}).
# "first": the visible text is the first argument, e.g.
#   {{nihongo|'''To You...'''|漢字|romaji}} -> '''To You...'''
# "last": the visible text is the last argument if there is more than one
#   (like [[target|display]]), or the only argument if there is just one:
#   {{w|Tetsurō Araki}} -> Tetsurō Araki
#   {{w|Sabu (director)|Hiroyuki Tanaka}} -> Hiroyuki Tanaka
CONTENT_TEMPLATE_ARG = {"nihongo": "first", "w": "last"}

# Sections to be completely discarded (heading and content), by exact name.
# They are removed for consistency and because sections like "Trivia" often
# reference future episodes (spoilers).
SECTIONS_TO_REMOVE = {
    "Characters in order of appearance",
    "Cast",
    "Soundtrack",
    "Trivia",
    "Navigation",
}

HEADER_PATTERN = re.compile(r"^(={2,6})\s*(.+?)\s*\1\s*$", re.MULTILINE)


def remove_comments(text: str) -> str:
    return COMMENT_PATTERN.sub("", text)


def expand_named_templates(text: str) -> str:
    """Replaces templates containing content with their visible text argument."""
    for name, which_arg in CONTENT_TEMPLATE_ARG.items():
        pattern = re.compile(r"\{\{\s*" + re.escape(name) + r"\s*\|([^{}]*)\}\}")

        def replace(match: re.Match[str], which_arg: str = which_arg) -> str:
            args = match.group(1).split("|")
            return args[0] if which_arg == "first" else args[-1]

        text = pattern.sub(replace, text)
    return text


def remove_sections(text: str) -> str:
    """Discard the sections listed in SECTIONS_TO_REMOVE, along with their content. 

    Removing a section at level N also discards its subsections
    (level > N), stopping at the next header with a level <= N.
    """
    lines = text.splitlines()
    result = []
    skip_level = None

    for line in lines:
        match = HEADER_PATTERN.match(line)
        if match:
            level, title = len(match.group(1)), match.group(2)
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and title in SECTIONS_TO_REMOVE:
                skip_level = level
                continue

        if skip_level is None:
            result.append(line)

    return "\n".join(result)


def remove_templates(text: str) -> str:
    """Removes {{...}} templates, including nested ones. 

    Repeatedly removes the "innermost" templates (those with no '{{' inside)
    until none remain, in order to handle nesting such as
    {{nihongo|'''text'''|{{w|kanji}}}}.
    """
    innermost_template = re.compile(r"\{\{[^{}]*\}\}")
    previous = None
    while previous != text:
        previous = text
        text = innermost_template.sub("", text)
    return text


def remove_file_links(text: str) -> str:
    """Removes complete image links ([[File:...]] / [[Image:...]]). 

    Unlike a standard link ([[target|display]] -> display), there is no
    text here worth preserving: the positional arguments relate to
    layout (thumb, left, right, 200px), and the image caption—which
    describes a visual scene—adds no new factual information to the text.
    """
    return FILE_LINK_PATTERN.sub("", text)


def convert_links(text: str) -> str:
    """[[target|display]] -> display; [[target]] -> target."""
    return LINK_PATTERN.sub(lambda m: m.group(2), text)


def remove_bold_italic(text: str) -> str:
    return BOLD_ITALIC_PATTERN.sub("", text)


def collapse_whitespace(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_wikitext(text: str) -> str:
    text = remove_comments(text)
    text = remove_sections(text)
    text = expand_named_templates(text)
    text = remove_templates(text)
    text = REF_PATTERN.sub("", text)
    text = HTML_TAG_PATTERN.sub("", text)
    text = remove_file_links(text)
    text = convert_links(text)
    text = remove_bold_italic(text)
    return collapse_whitespace(text)


def clean_directory(raw_subdir: str) -> None:
    input_dir = RAW_DIR / raw_subdir
    output_dir = PROCESSED_DIR / raw_subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    for raw_path in sorted(input_dir.glob("*.wikitext")):
        output_path = output_dir / f"{raw_path.stem}.txt"

        if output_path.exists():
            print(f"[skip] {output_path.name} ya existe")
            continue

        print(f"[clean] {raw_path.name}")
        cleaned = clean_wikitext(raw_path.read_text(encoding="utf-8"))
        output_path.write_text(cleaned, encoding="utf-8")


def main() -> None:
    clean_directory("episodes")
    clean_directory("characters")


if __name__ == "__main__":
    main()
