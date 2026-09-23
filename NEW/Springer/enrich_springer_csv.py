#!/usr/bin/env python3
"""
Enriquece um CSV exportado da Springer Nature Link com abstracts obtidos
do arquivo RIS usado pela opção "Cite this article".

Fluxo:
    CSV Springer -> DOI -> citation-needed Springer -> RIS -> campo AB -> CSV enriquecido

Características:
- Detecta automaticamente delimitador CSV/TSV/;.
- Preserva todas as colunas originais.
- Adiciona Abstract, RIS URL, status HTTP e status da coleta.
- Usa cache local dos arquivos RIS para permitir retomada sem baixar novamente.
- Faz retry de erros transitórios e respeita Retry-After.
- Não interrompe todo o processo quando um DOI falha.
- Pode ser executado novamente: registros já em cache são reutilizados.

Dependência:
    pip install requests
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://citation-needed.springer.com/v2/references/{doi}"
DEFAULT_DELAY = 1.0

DOI_COLUMNS = (
    "Item DOI",
    "DOI",
    "doi",
)

ABSTRACT_COLUMN = "Abstract"
RIS_URL_COLUMN = "RIS URL"
FETCH_STATUS_COLUMN = "Abstract Fetch Status"
HTTP_STATUS_COLUMN = "HTTP Status"


def normalize_doi(value: str) -> str:
    """Normaliza DOI vindo de CSV ou URL doi.org."""
    if value is None:
        return ""

    doi = str(value).strip()

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


def find_doi_column(fieldnames: List[str]) -> str:
    """Localiza a coluna que contém DOI."""
    normalized = {
        str(name).strip().lower(): name
        for name in fieldnames
        if name is not None
    }

    for candidate in DOI_COLUMNS:
        found = normalized.get(candidate.lower())
        if found:
            return found

    raise ValueError(
        "Não encontrei uma coluna de DOI. "
        f"Colunas disponíveis: {fieldnames}"
    )


def sniff_dialect(path: Path) -> csv.Dialect:
    """Tenta detectar comma, tab ou ponto e vírgula."""
    sample = path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    )[:10000]

    try:
        return csv.Sniffer().sniff(
            sample,
            delimiters=",;\t",
        )
    except csv.Error:
        return csv.excel


def create_session() -> requests.Session:
    """Cria sessão HTTP com retries para falhas transitórias."""
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=4,
        pool_maxsize=4,
    )

    session = requests.Session()

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": (
            "AcademicLiteratureReview/1.0 "
            "(Springer metadata enrichment; contact: local-script)"
        ),
        "Accept": (
            "text/plain,"
            "application/x-research-info-systems,"
            "*/*;q=0.8"
        ),
    })

    return session


def ris_cache_path(cache_dir: Path, doi: str) -> Path:
    """
    Gera nome estável e seguro para cache.
    Usa começo legível + hash para evitar colisões.
    """
    safe = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        doi,
    ).strip("_")

    digest = hashlib.sha1(
        doi.encode("utf-8")
    ).hexdigest()[:10]

    safe = safe[:100]

    return cache_dir / f"{safe}_{digest}.ris"


def parse_ris(text: str) -> Dict[str, List[str]]:
    """
    Parser RIS simples, preservando campos repetidos.

    Exemplo:
        AU  - Autor Um
        AU  - Autor Dois
        AB  - Abstract...
    """
    result: Dict[str, List[str]] = {}

    current_tag = None
    current_value = None

    def commit():
        nonlocal current_tag, current_value

        if current_tag is not None:
            value = (current_value or "").strip()

            result.setdefault(
                current_tag,
                [],
            ).append(value)

        current_tag = None
        current_value = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r\n")

        match = re.match(
            r"^([A-Z0-9]{2})  - ?(.*)$",
            line,
        )

        if match:
            commit()

            current_tag = match.group(1)
            current_value = match.group(2)

        elif current_tag is not None:
            # Continuação de campo RIS quebrado em múltiplas linhas.
            continuation = line.strip()

            if continuation:
                if current_value:
                    current_value += " " + continuation
                else:
                    current_value = continuation

    commit()

    return result


def first_ris_value(
    data: Dict[str, List[str]],
    tag: str,
) -> str:
    values = data.get(tag, [])

    if not values:
        return ""

    return values[0].strip()


def looks_like_ris(text: str) -> bool:
    """Evita salvar página HTML de erro como se fosse RIS."""
    head = text[:3000]

    return bool(
        re.search(
            r"(?m)^TY  - ",
            head,
        )
        and re.search(
            r"(?m)^ER  -",
            text,
        )
    )


def build_ris_url(doi: str) -> str:
    """
    Constrói URL apenas para registro no CSV.

    O slash do DOI é mantido, seguindo o formato observado
    nas URLs do botão de citação da Springer.
    """
    doi_path = quote(
        doi,
        safe="/",
    )

    return (
        BASE_URL.format(doi=doi_path)
        + "?format=refman&flavour=citation"
    )


def fetch_ris(
    session: requests.Session,
    doi: str,
    cache_dir: Path,
    timeout: float,
) -> Tuple[str, str, int | None, str]:
    """
    Retorna:
        ris_text,
        status lógico,
        HTTP status,
        URL
    """
    cache_file = ris_cache_path(
        cache_dir,
        doi,
    )

    url = build_ris_url(doi)

    if cache_file.exists():
        cached = cache_file.read_text(
            encoding="utf-8",
            errors="replace",
        )

        if looks_like_ris(cached):
            return (
                cached,
                "cached",
                None,
                url,
            )

    doi_path = quote(
        doi,
        safe="/",
    )

    endpoint = BASE_URL.format(
        doi=doi_path
    )

    response = session.get(
        endpoint,
        params={
            "format": "refman",
            "flavour": "citation",
        },
        timeout=timeout,
    )

    status_code = response.status_code

    if status_code != 200:
        return (
            "",
            f"http_error_{status_code}",
            status_code,
            response.url,
        )

    text = response.text

    if not looks_like_ris(text):
        return (
            "",
            "response_not_ris",
            status_code,
            response.url,
        )

    cache_file.write_text(
        text,
        encoding="utf-8",
    )

    return (
        text,
        "downloaded",
        status_code,
        response.url,
    )


def read_csv(path: Path):
    dialect = sniff_dialect(path)

    file_handle = path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    )

    reader = csv.DictReader(
        file_handle,
        dialect=dialect,
    )

    rows = list(reader)

    fieldnames = list(
        reader.fieldnames or []
    )

    file_handle.close()

    return rows, fieldnames, dialect


def write_csv(
    path: Path,
    rows: List[dict],
    fieldnames: List[str],
):
    """
    Saída padronizada em CSV separado por vírgula,
    UTF-8 com BOM para abrir bem no Excel.
    """
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Adiciona abstracts ao CSV exportado "
            "da Springer usando o RIS de citação por DOI."
        )
    )

    parser.add_argument(
        "input_csv",
        type=Path,
        help="CSV/TSV exportado da Springer.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help=(
            "CSV enriquecido de saída. "
            "Padrão: <arquivo>_with_abstracts.csv"
        ),
    )

    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("springer_ris_cache"),
        help=(
            "Pasta onde os RIS serão guardados "
            "para permitir retomada."
        ),
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=(
            "Pausa em segundos entre requisições "
            f"(padrão: {DEFAULT_DELAY})."
        ),
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout HTTP por requisição.",
    )

    args = parser.parse_args()

    input_csv = args.input_csv.resolve()

    if not input_csv.exists():
        raise SystemExit(
            f"ERRO: arquivo não encontrado: {input_csv}"
        )

    if args.output is None:
        output = input_csv.with_name(
            input_csv.stem
            + "_with_abstracts.csv"
        )
    else:
        output = args.output.resolve()

    cache_dir = args.cache_dir.resolve()

    cache_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows, original_fields, _ = read_csv(
        input_csv
    )

    if not rows:
        raise SystemExit(
            "ERRO: o arquivo não contém registros."
        )

    doi_column = find_doi_column(
        original_fields
    )

    extra_fields = [
        ABSTRACT_COLUMN,
        RIS_URL_COLUMN,
        FETCH_STATUS_COLUMN,
        HTTP_STATUS_COLUMN,
    ]

    fieldnames = list(
        original_fields
    )

    for field in extra_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    session = create_session()

    total = len(rows)
    found = 0
    missing_abstract = 0
    no_doi = 0
    errors = 0
    downloaded_requests = 0

    print(
        f"Registros encontrados: {total}"
    )

    print(
        f"Coluna DOI: {doi_column}"
    )

    print(
        f"Cache: {cache_dir}"
    )

    print()

    for index, row in enumerate(
        rows,
        start=1,
    ):
        doi = normalize_doi(
            row.get(doi_column, "")
        )

        title = (
            row.get("Item Title")
            or row.get("Title")
            or ""
        ).strip()

        prefix = (
            f"[{index:03d}/{total:03d}]"
        )

        if not doi:
            row[ABSTRACT_COLUMN] = ""
            row[RIS_URL_COLUMN] = ""
            row[FETCH_STATUS_COLUMN] = (
                "missing_doi"
            )
            row[HTTP_STATUS_COLUMN] = ""

            no_doi += 1

            print(
                f"{prefix} SEM DOI | "
                f"{title[:70]}"
            )

            continue

        try:
            ris_text, status, http_status, ris_url = fetch_ris(
                session=session,
                doi=doi,
                cache_dir=cache_dir,
                timeout=args.timeout,
            )

            row[RIS_URL_COLUMN] = ris_url
            row[HTTP_STATUS_COLUMN] = (
                ""
                if http_status is None
                else str(http_status)
            )

            if status == "downloaded":
                downloaded_requests += 1

            if not ris_text:
                row[ABSTRACT_COLUMN] = ""
                row[FETCH_STATUS_COLUMN] = status

                errors += 1

                print(
                    f"{prefix} ERRO "
                    f"{status} | {doi}"
                )

            else:
                ris = parse_ris(
                    ris_text
                )

                abstract = first_ris_value(
                    ris,
                    "AB",
                )

                if abstract:
                    row[ABSTRACT_COLUMN] = (
                        abstract
                    )
                    row[FETCH_STATUS_COLUMN] = (
                        status + "_abstract_ok"
                    )

                    found += 1

                    print(
                        f"{prefix} OK "
                        f"({len(abstract)} chars) "
                        f"| {doi}"
                    )

                else:
                    row[ABSTRACT_COLUMN] = ""
                    row[FETCH_STATUS_COLUMN] = (
                        status + "_no_abstract"
                    )

                    missing_abstract += 1

                    print(
                        f"{prefix} SEM ABSTRACT "
                        f"| {doi}"
                    )

        except requests.RequestException as exc:
            row[ABSTRACT_COLUMN] = ""
            row[RIS_URL_COLUMN] = build_ris_url(
                doi
            )
            row[FETCH_STATUS_COLUMN] = (
                "request_exception"
            )
            row[HTTP_STATUS_COLUMN] = ""

            errors += 1

            print(
                f"{prefix} ERRO HTTP | "
                f"{doi} | {exc}"
            )

        except Exception as exc:
            row[ABSTRACT_COLUMN] = ""
            row[RIS_URL_COLUMN] = build_ris_url(
                doi
            )
            row[FETCH_STATUS_COLUMN] = (
                "unexpected_error"
            )
            row[HTTP_STATUS_COLUMN] = ""

            errors += 1

            print(
                f"{prefix} ERRO | "
                f"{doi} | {exc}"
            )

        # Grava progresso após cada registro.
        # Se o script for interrompido, há uma saída parcial utilizável.
        write_csv(
            output,
            rows,
            fieldnames,
        )

        # Só aguarda quando houve download real.
        # Registros recuperados do cache não precisam de pausa.
        if (
            row.get(FETCH_STATUS_COLUMN, "")
            .startswith("downloaded")
            and args.delay > 0
            and index < total
        ):
            time.sleep(args.delay)

    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)

    print(
        f"Total de registros:       {total}"
    )
    print(
        f"Abstracts encontrados:    {found}"
    )
    print(
        f"RIS sem abstract:         {missing_abstract}"
    )
    print(
        f"Registros sem DOI:        {no_doi}"
    )
    print(
        f"Falhas HTTP/outros erros: {errors}"
    )
    print(
        f"Downloads nesta execução: {downloaded_requests}"
    )
    print(
        f"Arquivo de saída:         {output}"
    )

    if found + missing_abstract + no_doi + errors != total:
        print(
            "ATENÇÃO: as contagens finais "
            "não fecharam com o total."
        )

    print()
    print(
        "Os arquivos RIS originais foram "
        f"preservados em: {cache_dir}"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\nInterrompido pelo usuário. "
            "O cache já baixado será reutilizado "
            "na próxima execução.",
            file=sys.stderr,
        )
        raise SystemExit(130)
