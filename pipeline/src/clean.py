"""Limpia wikitext crudo y lo convierte a texto plano estructurado.

Quita templates ({{...}}), referencias (<ref>...</ref>), tags HTML,
comentarios y markup de enlaces/negritas, dejando prosa legible para
el chunking.

Limitación conocida: solo los templates listados en CONTENT_TEMPLATE_ARG
(nihongo, w) conservan su texto visible antes de que el resto de
templates se eliminen por completo. Si aparece otro template que también
envuelva prosa (no un campo estructurado tipo Infobox), hay que agregarlo
a esa lista; mientras tanto se pierde su contenido. Para el spike esto es
aceptable porque la revisión manual (Fase 5, paso 3 de PROJECT.md) audita
el resultado.
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

# Templates cuyo texto visible está en un argumento posicional, no en un
# campo estructurado (a diferencia de {{Infobox episode | Season = 1 | ...}}).
# "first": el texto visible es el primer argumento, p. ej.
#   {{nihongo|'''To You...'''|漢字|romaji}} -> '''To You...'''
# "last": el texto visible es el último argumento si hay más de uno
#   (como [[target|display]]), o el único argumento si solo hay uno:
#   {{w|Tetsurō Araki}} -> Tetsurō Araki
#   {{w|Sabu (director)|Hiroyuki Tanaka}} -> Hiroyuki Tanaka
CONTENT_TEMPLATE_ARG = {"nihongo": "first", "w": "last"}

# Secciones que se descartan por completo (encabezado y contenido), por nombre
# exacto. Se quitan por consistencia y porque secciones como "Trivia" suelen
# referenciar episodios futuros (spoilers).
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
    """Sustituye templates con contenido por su argumento de texto visible."""
    for name, which_arg in CONTENT_TEMPLATE_ARG.items():
        pattern = re.compile(r"\{\{\s*" + re.escape(name) + r"\s*\|([^{}]*)\}\}")

        def replace(match: re.Match[str], which_arg: str = which_arg) -> str:
            args = match.group(1).split("|")
            return args[0] if which_arg == "first" else args[-1]

        text = pattern.sub(replace, text)
    return text


def remove_sections(text: str) -> str:
    """Descarta las secciones listadas en SECTIONS_TO_REMOVE, con su contenido.

    Al quitar una sección de nivel N, también se descartan sus subsecciones
    (nivel > N), deteniéndose en el siguiente header de nivel <= N.
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
    """Elimina templates {{...}}, incluyendo los anidados.

    Quita repetidamente los templates "más internos" (sin '{{' dentro)
    hasta que no quede ninguno, para manejar anidación como
    {{nihongo|'''texto'''|{{w|kanji}}}}.
    """
    innermost_template = re.compile(r"\{\{[^{}]*\}\}")
    previous = None
    while previous != text:
        previous = text
        text = innermost_template.sub("", text)
    return text


def remove_file_links(text: str) -> str:
    """Elimina links a imágenes ([[File:...]] / [[Image:...]]) completos.

    A diferencia de un link normal ([[target|display]] -> display), aquí no
    hay texto que valga la pena conservar: los argumentos posicionales son
    de layout (thumb, left, right, 200px) y la leyenda de la imagen, que
    describe una escena visualmente, no aporta un hecho nuevo al texto.
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
