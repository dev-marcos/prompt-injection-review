#!/usr/bin/env python3
"""Divide arquivos BibTeX do IEEE S1 em lotes sequenciais.

Uso padrão:
    python split_ieee_bib.py

O script procura, no diretório informado, arquivos como:
    IEEE_S1_001-100.bib
    IEEE_S1_101-200.bib
    IEEE_S1_201-300.bib
    IEEE_S1_301-400.bib
    IEEE_S1_401-464.bib

e gera, por padrão, lotes de 20 registros em:
    IEEE_S1_batches_20/

Exemplo:
    IEEE_S1_batch_001-020.bib
    IEEE_S1_batch_021-040.bib
    ...
    IEEE_S1_batch_461-464.bib

Nenhuma deduplicação é feita nesta etapa; cada entrada BibTeX é preservada.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable


INPUT_PATTERN = "IEEE_S1_*.bib"
SOURCE_NAME_RE = re.compile(r"^IEEE_S1_(\d+)-(\d+)\.bib$", re.IGNORECASE)
ENTRY_KEY_RE = re.compile(r"@\s*[A-Za-z]+\s*[({]\s*([^,\s]+)", re.DOTALL)


def split_bibtex_entries(text: str) -> list[str]:
    """Extrai entradas BibTeX completas preservando o texto original.

    O parser usa balanceamento do delimitador externo ({...} ou (...)),
    portanto não depende de haver uma entrada por linha.
    """
    entries: list[str] = []
    n = len(text)
    pos = 0

    while pos < n:
        at = text.find("@", pos)
        if at == -1:
            break

        # Localiza o primeiro delimitador de abertura da entrada.
        brace = text.find("{", at)
        paren = text.find("(", at)
        openings = [x for x in (brace, paren) if x != -1]
        if not openings:
            break
        start_delim = min(openings)

        # Evita tratar um @ solto como início de entrada, exigindo um tipo válido.
        header = text[at:start_delim].strip()
        if not re.fullmatch(r"@[A-Za-z]+", header):
            pos = at + 1
            continue

        opener = text[start_delim]
        closer = "}" if opener == "{" else ")"
        depth = 0
        i = start_delim
        escaped = False

        while i < n:
            ch = text[i]

            if escaped:
                escaped = False
                i += 1
                continue

            if ch == "\\":
                escaped = True
                i += 1
                continue

            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    entries.append(text[at : i + 1].strip())
                    pos = i + 1
                    break

            i += 1
        else:
            raise ValueError(
                f"Entrada BibTeX iniciada na posição {at} não foi fechada corretamente."
            )

    return entries


def citation_key(entry: str) -> str:
    match = ENTRY_KEY_RE.search(entry)
    if not match:
        raise ValueError("Não foi possível identificar a chave de uma entrada BibTeX.")
    return match.group(1).strip()


def source_sort_key(path: Path) -> tuple[int, int, str]:
    match = SOURCE_NAME_RE.match(path.name)
    if match:
        return int(match.group(1)), int(match.group(2)), path.name.lower()
    return 10**12, 10**12, path.name.lower()


def chunks(items: list[str], size: int) -> Iterable[list[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Divide os BibTeX IEEE_S1 em lotes preservando as entradas originais."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("."),
        help="Pasta contendo os arquivos IEEE_S1_*.bib (padrão: pasta atual).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Pasta de saída (padrão: <input-dir>/IEEE_S1_batches_<batch-size>).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Quantidade de artigos por lote (padrão: 20).",
    )
    args = parser.parse_args()

    if args.batch_size <= 0:
        raise SystemExit("ERRO: --batch-size deve ser maior que zero.")

    input_dir = args.input_dir.resolve()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir is not None
        else input_dir / f"IEEE_S1_batches_{args.batch_size}"
    )

    if not input_dir.exists():
        raise SystemExit(f"ERRO: pasta de entrada não encontrada: {input_dir}")

    source_files = [
        p
        for p in input_dir.glob(INPUT_PATTERN)
        if p.is_file() and SOURCE_NAME_RE.match(p.name)
    ]
    source_files.sort(key=source_sort_key)

    if not source_files:
        raise SystemExit(
            f"ERRO: nenhum arquivo com nome IEEE_S1_<inicio>-<fim>.bib encontrado em {input_dir}"
        )

    print("Arquivos de origem encontrados:")
    for p in source_files:
        print(f"  - {p.name}")

    all_entries: list[str] = []
    per_file_counts: list[tuple[str, int]] = []

    for path in source_files:
        text = path.read_text(encoding="utf-8-sig", errors="strict")
        entries = split_bibtex_entries(text)
        if not entries:
            raise SystemExit(f"ERRO: nenhuma entrada BibTeX encontrada em {path.name}")
        all_entries.extend(entries)
        per_file_counts.append((path.name, len(entries)))

    original_keys = [citation_key(e) for e in all_entries]

    output_dir.mkdir(parents=True, exist_ok=True)

    # Remove apenas lotes antigos produzidos por este script, evitando arquivos obsoletos
    # caso o script seja executado novamente com outra quantidade de registros.
    for old_file in output_dir.glob("IEEE_S1_batch_*.bib"):
        old_file.unlink()

    output_files: list[Path] = []
    output_entries: list[str] = []

    for batch_index, batch in enumerate(chunks(all_entries, args.batch_size)):
        start = batch_index * args.batch_size + 1
        end = start + len(batch) - 1
        filename = f"IEEE_S1_batch_{start:03d}-{end:03d}.bib"
        output_path = output_dir / filename

        content = "\n\n".join(batch).rstrip() + "\n"
        output_path.write_text(content, encoding="utf-8", newline="\n")

        # Releitura para validar o arquivo efetivamente gravado.
        written = split_bibtex_entries(output_path.read_text(encoding="utf-8"))
        if len(written) != len(batch):
            raise RuntimeError(
                f"Falha de validação em {filename}: esperado {len(batch)}, encontrado {len(written)}."
            )

        output_files.append(output_path)
        output_entries.extend(written)

    output_keys = [citation_key(e) for e in output_entries]

    # Validação forte: mesma quantidade, mesmas chaves e mesma ordem.
    if original_keys != output_keys:
        raise RuntimeError(
            "Falha de validação: a sequência de chaves BibTeX da saída difere da entrada."
        )

    duplicate_keys = sorted({k for k in original_keys if original_keys.count(k) > 1})

    print("\nRegistros por arquivo de origem:")
    for name, count in per_file_counts:
        print(f"  {name}: {count}")

    print(f"\nTotal de registros lidos: {len(all_entries)}")
    print(f"Tamanho do lote: {args.batch_size}")
    print(f"Lotes gerados: {len(output_files)}")
    print(f"Pasta de saída: {output_dir}")

    print("\nArquivos gerados:")
    for path in output_files:
        count = len(split_bibtex_entries(path.read_text(encoding="utf-8")))
        print(f"  {path.name}: {count} artigos")

    if duplicate_keys:
        print("\nATENÇÃO: foram encontradas chaves BibTeX repetidas na entrada:")
        for key in duplicate_keys:
            print(f"  - {key}")
        print("Nenhuma foi removida; a deduplicação deve ser feita em outra etapa.")
    else:
        print("\nNenhuma chave BibTeX duplicada foi encontrada nos arquivos de entrada.")

    print("\nVALIDAÇÃO OK: nenhum registro foi perdido ou reordenado.")


if __name__ == "__main__":
    main()
