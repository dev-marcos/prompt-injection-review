#!/usr/bin/env python3
"""
baixar_pdfs_csv_v2.py

Versão 2 do downloader de PDFs acadêmicos.

Melhorias:
- tenta URL do CSV e DOI;
- consulta OpenAlex usando filtro de DOI;
- consulta Semantic Scholar por DOI;
- consulta Unpaywall (opcional, com e-mail);
- consulta Crossref;
- procura uma versão equivalente no arXiv pelo título;
- extrai citation_pdf_url de páginas das editoras;
- para IEEE, tenta descobrir o arnumber e usar stampPDF;
- para Springer, tenta o padrão /content/pdf/{doi}.pdf;
- valida se o conteúdo baixado é realmente PDF;
- gera download_log.csv detalhado;
- não contorna paywalls, autenticação ou CAPTCHA.

Dependências:
    pip install requests beautifulsoup4
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html
import re
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urlencode, urljoin

import requests
from bs4 import BeautifulSoup


DEFAULT_TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0 Safari/537.36"
)

ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    return html.unescape(str(value)).replace("\xa0", " ").strip()


def normalize_doi(value: str | None) -> str:
    doi = clean_text(value)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi.strip()


def normalize_title_for_match(text: str) -> str:
    text = clean_text(text).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_similarity(a: str, b: str) -> float:
    a_n = normalize_title_for_match(a)
    b_n = normalize_title_for_match(b)
    if not a_n or not b_n:
        return 0.0
    return difflib.SequenceMatcher(None, a_n, b_n).ratio()


def safe_filename(text: str, max_len: int = 150) -> str:
    text = clean_text(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._ ")
    return (text[:max_len] or "artigo").rstrip("._ ")


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
        }
    )
    return s


def unique_urls(urls: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for u in urls:
        u = clean_text(u)
        if not u or not u.lower().startswith(("http://", "https://")):
            continue
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def api_get_json(session, url, timeout):
    try:
        r = session.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def openalex_candidates(
    session: requests.Session, doi: str, timeout: int
) -> list[tuple[str, str]]:
    if not doi:
        return []

    # Filtro por DOI é mais robusto que codificar o DOI inteiro na rota /works/{id}.
    params = urlencode({"filter": f"doi:https://doi.org/{doi}", "per-page": 1})
    endpoint = f"https://api.openalex.org/works?{params}"
    data = api_get_json(session, endpoint, timeout)
    if not data:
        return []

    results = data.get("results") or []
    if not results:
        return []

    work = results[0]
    candidates = []

    def add_location(loc, label):
        if not isinstance(loc, dict):
            return
        pdf = loc.get("pdf_url")
        landing = loc.get("landing_page_url")
        if pdf:
            candidates.append((pdf, label))
        # Alguns repositórios entregam PDF quando a landing é um PDF.
        if landing and landing.lower().split("?")[0].endswith(".pdf"):
            candidates.append((landing, label + "_landing"))

    add_location(work.get("best_oa_location"), "openalex_best_oa")
    add_location(work.get("primary_location"), "openalex_primary")

    for loc in work.get("locations") or []:
        add_location(loc, "openalex_location")

    seen = set()
    out = []
    for url, label in candidates:
        if url not in seen:
            seen.add(url)
            out.append((url, label))
    return out


def semantic_scholar_candidates(
    session: requests.Session, doi: str, title: str, timeout: int
) -> list[tuple[str, str]]:
    candidates = []

    # Primeiro por DOI, se houver.
    if doi:
        endpoint = (
            "https://api.semanticscholar.org/graph/v1/paper/DOI:"
            + quote(doi, safe="")
            + "?fields=title,openAccessPdf,url,externalIds"
        )
        data = api_get_json(session, endpoint, timeout)
        if data:
            oa = data.get("openAccessPdf") or {}
            url = oa.get("url")
            if url:
                candidates.append((url, "semantic_scholar_oa"))

    # Fallback por título.
    if not candidates and title:
        params = urlencode(
            {
                "query": title,
                "limit": 5,
                "fields": "title,openAccessPdf,externalIds,url",
            }
        )
        endpoint = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
        data = api_get_json(session, endpoint, timeout)
        if data:
            best = None
            best_score = 0.0
            for item in data.get("data") or []:
                score = title_similarity(title, item.get("title") or "")
                if score > best_score:
                    best = item
                    best_score = score

            if best and best_score >= 0.90:
                oa = best.get("openAccessPdf") or {}
                url = oa.get("url")
                if url:
                    candidates.append((url, f"semantic_scholar_title_{best_score:.2f}"))

    return candidates


def unpaywall_candidates(
    session: requests.Session,
    doi: str,
    email: str | None,
    timeout: int,
) -> list[tuple[str, str]]:
    if not doi or not email:
        return []

    endpoint = (
        f"https://api.unpaywall.org/v2/{quote(doi, safe='')}"
        f"?email={quote(email)}"
    )
    data = api_get_json(session, endpoint, timeout)
    if not data:
        return []

    candidates = []
    best = data.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        candidates.append((best["url_for_pdf"], "unpaywall_best_oa"))

    for loc in data.get("oa_locations") or []:
        if isinstance(loc, dict) and loc.get("url_for_pdf"):
            candidates.append((loc["url_for_pdf"], "unpaywall_oa"))

    seen = set()
    out = []
    for url, label in candidates:
        if url not in seen:
            seen.add(url)
            out.append((url, label))
    return out


def crossref_candidates(
    session: requests.Session, doi: str, timeout: int
) -> list[tuple[str, str]]:
    if not doi:
        return []

    endpoint = "https://api.crossref.org/works/" + quote(doi, safe="")
    data = api_get_json(session, endpoint, timeout)
    if not data:
        return []

    msg = data.get("message") or {}
    candidates = []

    for item in msg.get("link") or []:
        if not isinstance(item, dict):
            continue
        url = item.get("URL")
        content_type = (item.get("content-type") or "").lower()
        if url and (
            "pdf" in content_type
            or url.lower().split("?")[0].endswith(".pdf")
        ):
            candidates.append((url, "crossref"))

    return candidates


def arxiv_candidates(
    session: requests.Session,
    title: str,
    timeout: int,
) -> list[tuple[str, str]]:
    if not title:
        return []

    # Busca arXiv por título. Retorna poucos resultados e valida similaridade.
    query = f'ti:"{title}"'
    params = urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": 5,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    endpoint = f"https://export.arxiv.org/api/query?{params}"

    try:
        r = session.get(endpoint, timeout=timeout)
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
    except Exception:
        return []

    matches = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        arxiv_title = clean_text(entry.findtext("atom:title", default="", namespaces=ARXIV_NS))
        score = title_similarity(title, arxiv_title)
        if score < 0.88:
            continue

        pdf_url = ""
        for link in entry.findall("atom:link", ARXIV_NS):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break

        if not pdf_url:
            entry_id = clean_text(entry.findtext("atom:id", default="", namespaces=ARXIV_NS))
            m = re.search(r"/abs/([^/?#]+)", entry_id)
            if m:
                pdf_url = f"https://arxiv.org/pdf/{m.group(1)}.pdf"

        if pdf_url:
            matches.append((score, pdf_url, arxiv_title))

    matches.sort(reverse=True, key=lambda x: x[0])
    if not matches:
        return []

    score, url, arxiv_title = matches[0]
    return [(url, f"arxiv_title_{score:.2f}")]


def publisher_pattern_candidates(
    doi: str, source: str
) -> list[tuple[str, str]]:
    if not doi:
        return []

    source_l = clean_text(source).lower()
    candidates = []

    if "springer" in source_l or doi.lower().startswith("10.1007/"):
        candidates.append(
            (f"https://link.springer.com/content/pdf/{doi}.pdf", "springer_pattern")
        )

    return candidates


def find_ieee_arnumber(text: str) -> str:
    patterns = [
        r"arnumber[=:\"'\s]+(\d{6,10})",
        r"/document/(\d{6,10})",
        r'"articleNumber"\s*:\s*"?(\d{6,10})"?',
        r'"arnumber"\s*:\s*"?(\d{6,10})"?',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.I)
        if m:
            return m.group(1)
    return ""


def extract_pdf_links_from_landing(
    session: requests.Session,
    landing_url: str,
    timeout: int,
) -> tuple[list[tuple[str, str]], str, str]:
    if not landing_url:
        return [], "", ""

    try:
        r = session.get(
            landing_url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8"
            },
        )
    except Exception:
        return [], "", ""

    final_url = r.url
    ctype = (r.headers.get("Content-Type") or "").lower()

    if "application/pdf" in ctype or b"%PDF-" in r.content[:4096]:
        return [(final_url, "landing_is_pdf")], final_url, ""

    if r.status_code != 200:
        return [], final_url, ""

    soup = BeautifulSoup(r.text, "html.parser")
    candidates = []

    # Metadados bibliográficos usuais.
    for meta in soup.find_all("meta"):
        name = clean_text(meta.get("name")).lower()
        prop = clean_text(meta.get("property")).lower()
        content = clean_text(meta.get("content"))
        if not content:
            continue

        if name == "citation_pdf_url" or prop == "citation_pdf_url":
            candidates.append((urljoin(final_url, content), "citation_pdf_url"))
        elif ".pdf" in content.lower() and name in {
            "dc.identifier",
            "eprints.document_url",
            "pdf_url",
            "wkhealth_pdf_url",
        }:
            candidates.append((urljoin(final_url, content), "meta_pdf"))

    for a in soup.find_all("a", href=True):
        href = clean_text(a.get("href"))
        label = clean_text(a.get_text(" ", strip=True)).lower()
        href_l = href.lower()

        if (
            ".pdf" in href_l
            or "download pdf" in label
            or label == "pdf"
            or "view pdf" in label
        ):
            candidates.append((urljoin(final_url, href), "page_pdf_link"))

    arnumber = find_ieee_arnumber(final_url + "\n" + r.text)
    if arnumber:
        candidates.extend(
            [
                (
                    f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={arnumber}",
                    "ieee_stamp_pdf",
                ),
                (
                    f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={arnumber}",
                    "ieee_stamp_page",
                ),
            ]
        )

    seen = set()
    out = []
    for url, label in candidates:
        if url not in seen:
            seen.add(url)
            out.append((url, label))

    return out, final_url, arnumber


def download_if_pdf(
    session: requests.Session,
    url: str,
    destination: Path,
    timeout: int,
    referer: str | None = None,
) -> tuple[bool, str, str]:
    headers = {"Accept": "application/pdf,*/*;q=0.8"}
    if referer:
        headers["Referer"] = referer

    try:
        with session.get(
            url,
            timeout=timeout,
            stream=True,
            allow_redirects=True,
            headers=headers,
        ) as r:
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}", r.url

            iterator = r.iter_content(chunk_size=64 * 1024)
            try:
                first = next(iterator)
            except StopIteration:
                return False, "resposta vazia", r.url

            ctype = (r.headers.get("Content-Type") or "").lower()
            is_pdf = b"%PDF-" in first[:8192] or "application/pdf" in ctype

            if not is_pdf:
                snippet = first[:200].decode("utf-8", errors="ignore").replace("\n", " ")
                return (
                    False,
                    f"não é PDF (Content-Type: {ctype or 'desconhecido'}; início={snippet[:100]!r})",
                    r.url,
                )

            temp = destination.with_suffix(destination.suffix + ".part")
            with open(temp, "wb") as f:
                f.write(first)
                for chunk in iterator:
                    if chunk:
                        f.write(chunk)

            if temp.stat().st_size < 1000:
                temp.unlink(missing_ok=True)
                return False, "arquivo PDF muito pequeno/suspeito", r.url

            # Verificação final da assinatura.
            with open(temp, "rb") as f:
                head = f.read(16)
            if b"%PDF-" not in head:
                temp.unlink(missing_ok=True)
                return False, "assinatura PDF ausente", r.url

            temp.replace(destination)
            return True, "ok", r.url

    except requests.RequestException as exc:
        return False, f"{type(exc).__name__}: {exc}", url
    except Exception as exc:
        return False, f"erro: {exc}", url


def load_rows(csv_path: Path) -> list[dict]:
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    def sort_key(row: dict):
        raw = clean_text(row.get("selection_priority"))
        try:
            return int(float(raw))
        except Exception:
            return 10**9

    return sorted(rows, key=sort_key)


def process_article(
    session: requests.Session,
    row: dict,
    output_dir: Path,
    timeout: int,
    unpaywall_email: str | None,
    overwrite: bool,
    delay: float,
) -> dict:
    priority_raw = clean_text(row.get("selection_priority"))
    try:
        priority = int(float(priority_raw))
    except Exception:
        priority = 0

    title = clean_text(row.get("title")) or "Sem titulo"
    doi = normalize_doi(row.get("doi"))
    csv_url = clean_text(row.get("url"))
    source = clean_text(row.get("sources"))

    prefix = f"{priority:02d}" if priority else "00"
    destination = output_dir / f"{prefix}_{safe_filename(title)}.pdf"

    log = {
        "selection_priority": priority_raw,
        "title": title,
        "doi": doi,
        "status": "",
        "pdf_file": "",
        "source_method": "",
        "download_url": "",
        "landing_url": "",
        "ieee_arnumber": "",
        "details": "",
    }

    if destination.exists() and not overwrite:
        log["status"] = "JA_EXISTE"
        log["pdf_file"] = str(destination)
        log["details"] = "Arquivo já existe; use --overwrite para baixar novamente."
        return log

    # Candidatos obtidos de fontes públicas.
    candidates: list[tuple[str, str]] = []

    candidates.extend(openalex_candidates(session, doi, timeout))
    candidates.extend(semantic_scholar_candidates(session, doi, title, timeout))
    candidates.extend(unpaywall_candidates(session, doi, unpaywall_email, timeout))
    candidates.extend(crossref_candidates(session, doi, timeout))
    candidates.extend(arxiv_candidates(session, title, timeout))
    candidates.extend(publisher_pattern_candidates(doi, source))

    if csv_url and ".pdf" in csv_url.lower():
        candidates.insert(0, (csv_url, "csv_direct_pdf"))

    # Deduplica URLs preservando a origem.
    deduped = []
    seen = set()
    for url, method in candidates:
        url = clean_text(url)
        if url and url not in seen:
            seen.add(url)
            deduped.append((url, method))

    errors = []

    for candidate, method in deduped:
        ok, detail, final_url = download_if_pdf(
            session, candidate, destination, timeout
        )
        if ok:
            log["status"] = "BAIXADO"
            log["pdf_file"] = str(destination)
            log["source_method"] = method
            log["download_url"] = final_url
            log["details"] = "PDF obtido por fonte pública."
            time.sleep(delay)
            return log

        errors.append(f"{method}: {candidate} -> {detail}")

    # Landing pages: URL do CSV e DOI.
    landing_pages = []
    if csv_url:
        landing_pages.append(csv_url)
    if doi:
        landing_pages.append(f"https://doi.org/{doi}")

    for landing in unique_urls(landing_pages):
        pdf_links, final_landing, arnumber = extract_pdf_links_from_landing(
            session, landing, timeout
        )

        if final_landing:
            log["landing_url"] = final_landing
        if arnumber:
            log["ieee_arnumber"] = arnumber

        for candidate, method in pdf_links:
            ok, detail, final_url = download_if_pdf(
                session,
                candidate,
                destination,
                timeout,
                referer=final_landing or landing,
            )
            if ok:
                log["status"] = "BAIXADO"
                log["pdf_file"] = str(destination)
                log["source_method"] = method
                log["download_url"] = final_url
                log["details"] = (
                    f"PDF localizado a partir da landing page "
                    f"{final_landing or landing}"
                )
                time.sleep(delay)
                return log

            errors.append(f"{method}: {candidate} -> {detail}")

    log["status"] = "NAO_BAIXADO"
    log["details"] = (
        "Não foi encontrada uma cópia PDF pública acessível automaticamente. "
        "O artigo pode exigir acesso institucional/login ou download manual."
    )
    if errors:
        log["details"] += " Tentativas: " + " | ".join(errors[:12])

    time.sleep(delay)
    return log


def write_log(log_path: Path, records: list[dict]) -> None:
    fields = [
        "selection_priority",
        "title",
        "doi",
        "status",
        "pdf_file",
        "source_method",
        "download_url",
        "landing_url",
        "ieee_arnumber",
        "details",
    ]
    with open(log_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Baixa versões PDF públicas usando DOI, URL, OpenAlex, "
            "Semantic Scholar, arXiv, Crossref, Unpaywall e editoras."
        )
    )
    parser.add_argument("csv", type=Path, help="CSV de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("03_pdfs"),
        help="Pasta de saída dos PDFs (padrão: ./03_pdfs)",
    )
    parser.add_argument(
        "--unpaywall-email",
        default=None,
        help="E-mail para consultar a API do Unpaywall (opcional, recomendado).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout HTTP em segundos (padrão: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Pausa em segundos entre artigos (padrão: 1.0)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve PDFs que já existem.",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"ERRO: CSV não encontrado: {args.csv}", file=sys.stderr)
        return 2

    args.output.mkdir(parents=True, exist_ok=True)
    log_path = args.output / "download_log_v2.csv"

    rows = load_rows(args.csv)
    session = make_session()

    print(f"Registros encontrados: {len(rows)}")
    print(f"Pasta de saída: {args.output.resolve()}")
    print()

    logs = []

    for idx, row in enumerate(rows, start=1):
        priority = clean_text(row.get("selection_priority")) or str(idx)
        title = clean_text(row.get("title"))
        print(f"[{idx}/{len(rows)}] Prioridade {priority}: {title}")

        result = process_article(
            session=session,
            row=row,
            output_dir=args.output,
            timeout=args.timeout,
            unpaywall_email=args.unpaywall_email,
            overwrite=args.overwrite,
            delay=args.delay,
        )
        logs.append(result)

        print(f"    -> {result['status']}")
        if result["source_method"]:
            print(f"       fonte: {result['source_method']}")
        if result["download_url"]:
            print(f"       {result['download_url']}")

        # Salva progresso a cada artigo.
        write_log(log_path, logs)

    baixados = sum(r["status"] == "BAIXADO" for r in logs)
    existentes = sum(r["status"] == "JA_EXISTE" for r in logs)
    falhas = sum(r["status"] == "NAO_BAIXADO" for r in logs)

    print()
    print("Concluído.")
    print(f"Baixados agora: {baixados}")
    print(f"Já existentes:   {existentes}")
    print(f"Não baixados:    {falhas}")
    print(f"Log detalhado:   {log_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
