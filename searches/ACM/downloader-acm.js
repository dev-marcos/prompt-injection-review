(() => {
    console.clear();

    const BASE_URL = "https://dl.acm.org";
    const ITEM_SELECTOR = "li.search__item.issue-item-container";

    // =========================================================
    // FUNÇÕES AUXILIARES
    // =========================================================

    function cleanText(element) {
        if (!element) return "";

        return (element.innerText || "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function escapeBibTeX(text) {
        if (!text) return "";

        return String(text)
            .replace(/\\/g, "\\\\")
            .replace(/([{}])/g, "\\$1");
    }

    function getYear(dateText) {
        if (!dateText) return "";

        const match = dateText.match(/\b(19|20)\d{2}\b/);

        return match ? match[0] : "";
    }

    function getBibTeXKey(article, index) {
        let author = "unknown";

        if (
            article.authors &&
            article.authors.length > 0
        ) {
            author = article.authors[0]
                .split(/\s+/)
                .pop();
        }

        author = author
            .replace(/[^a-zA-ZÀ-ÿ0-9]/g, "")
            .toLowerCase();

        const year = getYear(
            article.published_date || article.date
        );

        let doiPart = "";

        if (article.doi) {
            doiPart = article.doi
                .split("/")
                .pop()
                .replace(/[^a-zA-Z0-9]/g, "");
        }

        return `${author}${year}${doiPart || index + 1}`;
    }

    // =========================================================
    // QUANTIDADE DE RESULTADOS
    // =========================================================

    const hitsElement =
        document.querySelector(".hitsLength");

    let totalResults = null;

    if (hitsElement) {
        const match = cleanText(hitsElement)
            .match(/\d+/);

        if (match) {
            totalResults = parseInt(
                match[0],
                10
            );
        }
    }

    // =========================================================
    // LOCALIZAR ARTIGOS
    // =========================================================

    const items = [
        ...document.querySelectorAll(
            ITEM_SELECTOR
        )
    ];

    console.log(
        `Resultados encontrados: ${items.length}`
    );

    if (totalResults !== null) {
        console.log(
            `Resultados informados pelo ACM: ${totalResults}`
        );
    }

    // =========================================================
    // EXTRAIR ARTIGOS
    // =========================================================

    const articles = items.map((item, index) => {

        // -------------------------
        // TÍTULO
        // -------------------------

        const titleElement =
            item.querySelector(
                "h4.issue-item__title a"
            );

        const title =
            cleanText(titleElement);

        // -------------------------
        // URL
        // -------------------------

        let url = "";

        if (titleElement) {
            const href =
                titleElement.getAttribute("href");

            if (href) {
                url = new URL(
                    href,
                    BASE_URL
                ).href;
            }
        }

        // -------------------------
        // DOI
        // -------------------------

        const doiElement =
            item.querySelector(
                "a.issue-item__doi"
            );

        let doi =
            cleanText(doiElement);

        doi = doi
            .replace(
                /^https?:\/\/doi\.org\//i,
                ""
            )
            .trim();

        // -------------------------
        // AUTORES
        // -------------------------

        const authorElements = [
            ...item.querySelectorAll(
                ".hlFld-ContribAuthor span"
            )
        ];

        const authors = [
            ...new Set(
                authorElements
                    .map(cleanText)
                    .filter(Boolean)
            )
        ];

        // -------------------------
        // ABSTRACT
        // -------------------------

        const abstractElement =
            item.querySelector(
                ".issue-item__abstract"
            );

        const abstract =
            cleanText(abstractElement);

        // -------------------------
        // DATA
        // -------------------------

        const dateElement =
            item.querySelector(
                ".bookPubDate"
            );

        const date =
            cleanText(dateElement);

        const publishedDate =
            dateElement?.getAttribute(
                "data-title"
            ) || "";

        // -------------------------
        // TIPO
        // -------------------------

        const typeElement =
            item.querySelector(
                ".issue-heading"
            );

        const type =
            cleanText(typeElement);

        // -------------------------
        // PUBLICAÇÃO
        // -------------------------

        const publicationElement =
            item.querySelector(
                ".epub-section__title"
            );

        const publication =
            cleanText(publicationElement);

        return {
            index: index + 1,
            title,
            authors,
            abstract,
            doi,
            url,
            date,
            published_date: publishedDate,
            type,
            publication
        };
    });

    // =========================================================
    // REMOVER DUPLICADOS POR DOI
    // =========================================================

    const seen = new Set();

    const uniqueArticles =
        articles.filter(article => {

            if (!article.doi) {
                return true;
            }

            const normalized =
                article.doi.toLowerCase();

            if (seen.has(normalized)) {
                return false;
            }

            seen.add(normalized);

            return true;
        });

    // =========================================================
    // GERAR BIBTEX
    // =========================================================

    const entries = [];

    uniqueArticles.forEach(
        (article, index) => {

            if (!article.doi) {
                console.warn(
                    `Artigo sem DOI: ${article.title}`
                );
            }

            const key =
                getBibTeXKey(
                    article,
                    index
                );

            const year =
                getYear(
                    article.published_date ||
                    article.date
                );

            // Autores
            let authorField = "";

            if (
                article.authors &&
                article.authors.length
            ) {
                authorField =
                    article.authors
                        .map(escapeBibTeX)
                        .join(" and ");
            }

            // Montar entrada
            const entry = `@article{${key},
  title = {${escapeBibTeX(article.title)}},
  author = {${authorField}},
  year = {${year}},
  doi = {${escapeBibTeX(article.doi)}},
  url = {${escapeBibTeX(article.url)}},
  journal = {${escapeBibTeX(article.publication)}}
}`;

            entries.push(entry);
        }
    );

    // =========================================================
    // CABEÇALHO DO ARQUIVO
    // =========================================================

    const header = `% BibTeX generated from ACM Digital Library
% Search date: ${new Date().toISOString()}
% Results reported by ACM: ${totalResults ?? "unknown"}
% Results extracted: ${articles.length}
% Unique results: ${uniqueArticles.length}

`;

    const bibtex =
        header +
        entries.join("\n\n") +
        "\n";

    // =========================================================
    // DOWNLOAD
    // =========================================================

    const blob = new Blob(
        [bibtex],
        {
            type: "application/x-bibtex;charset=utf-8"
        }
    );

    const downloadUrl =
        URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    link.href = downloadUrl;

    link.download =
        "acm_digital_library_results.bib";

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(downloadUrl);

    // =========================================================
    // RELATÓRIO
    // =========================================================

    console.log("");
    console.log(
        "=========================================="
    );
    console.log(
        "       ACM → BIBTEX"
    );
    console.log(
        "=========================================="
    );

    console.log(
        `Resultados informados: ${totalResults}`
    );

    console.log(
        `Resultados encontrados: ${articles.length}`
    );

    console.log(
        `Resultados únicos: ${uniqueArticles.length}`
    );

    console.log(
        `Entradas BibTeX: ${entries.length}`
    );

    console.log(
        "=========================================="
    );

    if (
        totalResults !== null &&
        articles.length === totalResults
    ) {
        console.log(
            "✅ Todos os resultados foram extraídos."
        );
    } else if (
        totalResults !== null
    ) {
        console.warn(
            `⚠️ Atenção: ACM informa ${totalResults}, ` +
            `mas foram encontrados ${articles.length}.`
        );
    }

    console.log(
        "📥 Arquivo acm_digital_library_results.bib baixado."
    );

})();