#!/usr/bin/env python3
"""
Converte o CSV enriquecido da Springer para arquivos BibTeX em lotes.

Entrada esperada (nomes típicos do CSV da Springer):
    Item Title
    Publication Title
    Book Series Title
    Journal Volume
    Journal Issue
    Item DOI
    Authors
    Publication Year
    URL
    Content Type
    Abstract

Saída padrão:
    SPRINGER_S1_batches_20/
        SPRINGER_S1_batch_001-020.bib
        SPRINGER_S1_batch_021-040.bib
        ...

Uso:
    python springer_csv_to_bib_batches.py springer_with_abstracts.csv

Opcional:
    python springer_csv_to_bib_batches.py springer_with_abstracts.csv --batch-size 20
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path
from typing import Dict, List


def sniff_dialect(path: Path) -> csv.Dialect:
    sample = path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    )[:20000]

    try:
        return csv.Sniffer().sniff(
            sample,
            delimiters=",;\t",
        )
    except csv.Error:
        return csv.excel


def clean(value) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def bib_escape(value: str) -> str:
    """
    Escapa apenas caracteres que podem quebrar o BibTeX,
    preservando Unicode para facilitar leitura pelo ChatGPT.
    """
    value = clean(value)
    value = value.replace("\\", r"\\")
    value = value.replace("{", r"\{")
    value = value.replace("}", r"\}")
    return value


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        ch for ch in value
        if not unicodedata.combining(ch)
    )
    value = re.sub(r"[^A-Za-z0-9]+", "", value)
    return value


def normalize_doi(value: str) -> str:
    doi = clean(value)

    doi = re.sub(
        r"^https?://(?:dx\.)?doi\.org/",
        "",
        doi,
        flags=re.IGNORECASE,
    )

    doi = re.sub(
        r"^doi:\s*",
        "",
        doi,
        flags=re.IGNORECASE,
    )

    return doi.strip()


def parse_authors(raw: str) -> List[str]:
    """
    O CSV da Springer às vezes exporta autores sem um delimitador claro.
    Não tenta adivinhar nomes quando não há separação confiável.

    Se já houver ';' ou '|' entre autores, converte para ' and ' do BibTeX.
    Caso contrário, preserva o texto original como um único campo author.
    """
    raw = clean(raw)

    if not raw:
        return []

    if ";" in raw:
        return [
            clean(x)
            for x in raw.split(";")
            if clean(x)
        ]

    if "|" in raw:
        return [
            clean(x)
            for x in raw.split("|")
            if clean(x)
        ]

    return [raw]


def choose_entry_type(content_type: str) -> str:
    ct = clean(content_type).lower()

    if "chapter" in ct:
        return "incollection"

    if "conference" in ct:
        return "inproceedings"

    if "article" in ct:
        return "article"

    if "book" in ct:
        return "book"

    return "misc"


def make_key(
    row: Dict[str, str],
    sequential_id: int,
) -> str:
    """
    Gera chave BibTeX estável e única.
    Ex.: SPRINGER_0001_Torrielli2026
    """
    year = clean(
        row.get("Publication Year", "")
    )

    authors = clean(
        row.get("Authors", "")
    )

    first_author_token = ""

    if authors:
        token = re.split(
            r"[;|,\s]+",
            authors,
        )[0]

        first_author_token = slugify(token)

    suffix = (
        f"_{first_author_token}{year}"
        if first_author_token or year
        else ""
    )

    return (
        f"SPRINGER_{sequential_id:04d}"
        f"{suffix}"
    )


def add_field(
    fields: List[tuple],
    name: str,
    value: str,
):
    value = clean(value)

    if value:
        fields.append(
            (name, bib_escape(value))
        )


def row_to_bib(
    row: Dict[str, str],
    sequential_id: int,
) -> str:
    entry_type = choose_entry_type(
        row.get("Content Type", "")
    )

    key = make_key(
        row,
        sequential_id,
    )

    title = clean(
        row.get("Item Title", "")
    )

    publication_title = clean(
        row.get("Publication Title", "")
    )

    book_series = clean(
        row.get("Book Series Title", "")
    )

    doi = normalize_doi(
        row.get("Item DOI", "")
    )

    authors = parse_authors(
        row.get("Authors", "")
    )

    author_field = " and ".join(authors)

    fields: List[tuple] = []

    add_field(fields, "title", title)
    add_field(fields, "author", author_field)
    add_field(
        fields,
        "year",
        row.get("Publication Year", ""),
    )
    add_field(
        fields,
        "abstract",
        row.get("Abstract", ""),
    )
    add_field(fields, "doi", doi)
    add_field(
        fields,
        "url",
        row.get("URL", ""),
    )
    add_field(
        fields,
        "volume",
        row.get("Journal Volume", ""),
    )
    add_field(
        fields,
        "number",
        row.get("Journal Issue", ""),
    )

    if entry_type == "article":
        add_field(
            fields,
            "journal",
            publication_title,
        )

    elif entry_type in {
        "incollection",
        "inproceedings",
    }:
        add_field(
            fields,
            "booktitle",
            publication_title,
        )

        add_field(
            fields,
            "series",
            book_series,
        )

    elif entry_type == "book":
        add_field(
            fields,
            "series",
            book_series,
        )

    else:
        add_field(
            fields,
            "howpublished",
            publication_title,
        )

        add_field(
            fields,
            "series",
            book_series,
        )

    add_field(
        fields,
        "type",
        row.get("Content Type", ""),
    )

    # Campos auxiliares úteis para rastreabilidade da revisão.
    add_field(
        fields,
        "database",
        "Springer Nature Link",
    )

    add_field(
        fields,
        "searchid",
        "SPRINGER_S1",
    )

    lines = [
        f"@{entry_type.upper()}{{{key},"
    ]

    for index, (name, value) in enumerate(fields):
        comma = "," if index < len(fields) - 1 else ""
        lines.append(
            f"  {name} = {{{value}}}{comma}"
        )

    lines.append("}")

    return "\n".join(lines)


def read_csv(path: Path):
    dialect = sniff_dialect(path)

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        reader = csv.DictReader(
            f,
            dialect=dialect,
        )

        rows = list(reader)
        fieldnames = list(
            reader.fieldnames or []
        )

    return rows, fieldnames


def validate_required_columns(
    fieldnames: List[str],
):
    required = {
        "Item Title",
        "Publication Year",
        "Item DOI",
        "URL",
        "Abstract",
    }

    missing = sorted(
        required - set(fieldnames)
    )

    if missing:
        raise ValueError(
            "O CSV não contém as colunas obrigatórias: "
            + ", ".join(missing)
        )


def chunks(items: List[str], size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Converte CSV enriquecido da Springer "
            "para BibTeX em lotes."
        )
    )

    parser.add_argument(
        "input_csv",
        type=Path,
        help="CSV enriquecido com a coluna Abstract.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Número de artigos por lote. Padrão: 20.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Pasta de saída. "
            "Padrão: SPRINGER_S1_batches_<batch-size>"
        ),
    )

    parser.add_argument(
        "--skip-without-abstract",
        action="store_true",
        help=(
            "Ignora registros sem abstract. "
            "Por padrão eles são preservados."
        ),
    )

    args = parser.parse_args()

    if args.batch_size <= 0:
        raise SystemExit(
            "ERRO: --batch-size deve ser maior que zero."
        )

    input_csv = args.input_csv.resolve()

    if not input_csv.exists():
        raise SystemExit(
            f"ERRO: arquivo não encontrado: {input_csv}"
        )

    if args.output_dir is None:
        output_dir = (
            input_csv.parent
            / f"SPRINGER_S1_batches_{args.batch_size}"
        )
    else:
        output_dir = args.output_dir.resolve()

    rows, fieldnames = read_csv(input_csv)

    validate_required_columns(
        fieldnames
    )

    if args.skip_without_abstract:
        original_count = len(rows)

        rows = [
            row
            for row in rows
            if clean(row.get("Abstract", ""))
        ]

        print(
            f"Registros sem abstract removidos: "
            f"{original_count - len(rows)}"
        )

    if not rows:
        raise SystemExit(
            "ERRO: nenhum registro para converter."
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Limpa apenas os batches antigos gerados pelo script.
    for old in output_dir.glob(
        "SPRINGER_S1_batch_*.bib"
    ):
        old.unlink()

    entries = []

    without_abstract = 0
    without_doi = 0

    for index, row in enumerate(
        rows,
        start=1,
    ):
        if not clean(
            row.get("Abstract", "")
        ):
            without_abstract += 1

        if not normalize_doi(
            row.get("Item DOI", "")
        ):
            without_doi += 1

        entries.append(
            row_to_bib(
                row,
                sequential_id=index,
            )
        )

    generated_files = []

    for batch_index, batch in enumerate(
        chunks(entries, args.batch_size)
    ):
        start = (
            batch_index * args.batch_size
            + 1
        )

        end = (
            start + len(batch) - 1
        )

        filename = (
            f"SPRINGER_S1_batch_"
            f"{start:03d}-{end:03d}.bib"
        )

        output_path = (
            output_dir / filename
        )

        content = (
            "\n\n".join(batch)
            + "\n"
        )

        output_path.write_text(
            content,
            encoding="utf-8",
            newline="\n",
        )

        generated_files.append(
            (output_path, len(batch))
        )

    # Validação simples: conta início de entradas.
    written_total = 0

    for path, expected_count in generated_files:
        content = path.read_text(
            encoding="utf-8"
        )

        actual_count = len(
            re.findall(
                r"(?m)^@[A-Z]+\{",
                content,
            )
        )

        if actual_count != expected_count:
            raise RuntimeError(
                f"Falha de validação em {path.name}: "
                f"esperado {expected_count}, "
                f"encontrado {actual_count}."
            )

        written_total += actual_count

    if written_total != len(entries):
        raise RuntimeError(
            "Falha de validação: número total "
            "de entradas escritas não corresponde "
            "ao número de registros do CSV."
        )

    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)

    print(
        f"Registros no CSV:          {len(rows)}"
    )

    print(
        f"Sem abstract:              {without_abstract}"
    )

    print(
        f"Sem DOI:                   {without_doi}"
    )

    print(
        f"Tamanho do lote:           {args.batch_size}"
    )

    print(
        f"Lotes gerados:             {len(generated_files)}"
    )

    print(
        f"Entradas BibTeX geradas:   {written_total}"
    )

    print(
        f"Pasta de saída:            {output_dir}"
    )

    print()
    print("Arquivos:")

    for path, count in generated_files:
        print(
            f"  {path.name}: {count} artigos"
        )

    print()
    print(
        "VALIDAÇÃO OK: todos os registros "
        "foram convertidos para BibTeX."
    )


if __name__ == "__main__":
    main()
