(async () => {

    // ============================================================
    // CONFIGURAÇÃO
    // ============================================================

    const T =
        "9874b53b2da0b6aad6d68ce17e2f20a4d574da688ee85925ba3a66a84345d701d6a7a6d4bac5594624d77bab6de3541f7050f82be2886ce4462db44f4a45b94ae4faad742b0a3f9c624b35f782339fdb155adef62fb98ffe4098bf933cb478aa14cbf85106eba2be3cae9a054f2bb164";

    // Máximo permitido pelo ScienceDirect
    const SHOW = 100;

    // Delay normal entre requisições
    const DELAY_BETWEEN_REQUESTS = 8000;

    // Delay inicial após HTTP 429
    const DELAY_429 = 30000;

    // Máximo de tentativas para uma requisição
    const MAX_RETRIES = 5;


    // ============================================================
    // QUERIES
    // ============================================================

    const queries = [

        {
            id: "Q01",
            name: "Prompt injection + LLM",
            qs: '"prompt injection" AND "large language model"'
        },

        {
            id: "Q02",
            name: "Prompt injection + NER",
            qs: '"prompt injection" AND ("named entity recognition" OR NER)'
        },

        {
            id: "Q03",
            name: "Prompt injection + entity extraction",
            qs: '"prompt injection" AND "entity extraction"'
        },

        {
            id: "Q04",
            name: "Prompt injection + information extraction",
            qs: '"prompt injection" AND "information extraction"'
        },

        {
            id: "Q05",
            name: "Indirect prompt injection",
            qs: '"indirect prompt injection"'
        },

        {
            id: "Q06",
            name: "Direct prompt injection",
            qs: '"direct prompt injection"'
        },

        {
            id: "Q07",
            name: "Prompt injection + RAG",
            qs: '"prompt injection" AND (RAG OR "retrieval augmented generation")'
        },

        {
            id: "Q08",
            name: "Instruction hijacking",
            qs: '"instruction hijacking"'
        },

        {
            id: "Q09",
            name: "Prompt hijacking",
            qs: '"prompt hijacking"'
        }

    ];


    // ============================================================
    // ESTADO GLOBAL
    // ============================================================

    const state = {

        startedAt:
            new Date().toISOString(),

        queries: [],

        totalRequests: 0,

        total429: 0,

        rawResults: [],

        uniqueResults: []
    };


    window.sciencedirectState = state;


    // ============================================================
    // SLEEP
    // ============================================================

    function sleep(ms) {

        return new Promise(
            resolve => setTimeout(resolve, ms)
        );
    }


    // ============================================================
    // CONSTRUIR URL
    // ============================================================

    function buildUrl(
        qs,
        offset = 0
    ) {

        let url =
            "https://www.sciencedirect.com/search/api" +
            "?qs=" +
            encodeURIComponent(qs) +
            "&show=" +
            SHOW;

        if (offset > 0) {

            url +=
                "&offset=" +
                offset;
        }

        url +=
            "&t=" +
            T +
            "&hostname=www.sciencedirect.com" +
            "&navigation=true";

        return url;
    }


    // ============================================================
    // REQUISIÇÃO COM RETRY / BACKOFF
    // ============================================================

    async function request(
        qs,
        offset
    ) {

        let retry = 0;

        while (
            retry <= MAX_RETRIES
        ) {

            const url =
                buildUrl(
                    qs,
                    offset
                );


            console.log("");
            console.log(
                `🌐 Request #${state.totalRequests + 1}`
            );

            console.log(
                `offset=${offset} | show=${SHOW}`
            );


            state.totalRequests++;


            try {

                const response =
                    await fetch(
                        url,
                        {
                            credentials:
                                "include"
                        }
                    );


                console.log(
                    `HTTP: ${response.status}`
                );


                // ------------------------------------------------
                // 429
                // ------------------------------------------------

                if (
                    response.status === 429
                ) {

                    state.total429++;


                    retry++;


                    if (
                        retry >
                        MAX_RETRIES
                    ) {

                        console.error(
                            "❌ Número máximo de retries atingido."
                        );

                        return {
                            ok: false,
                            status: 429,
                            data: null,
                            url
                        };
                    }


                    const wait =
                        DELAY_429 *
                        Math.pow(
                            2,
                            retry - 1
                        );


                    console.warn(
                        `🚦 HTTP 429 - Too Many Requests`
                    );

                    console.warn(
                        `⏳ Esperando ${wait / 1000}s antes de tentar novamente...`
                    );


                    await sleep(
                        wait
                    );


                    continue;
                }


                // ------------------------------------------------
                // Outros erros
                // ------------------------------------------------

                if (
                    !response.ok
                ) {

                    const text =
                        await response.text();


                    console.error(
                        `❌ HTTP ${response.status}`
                    );


                    console.error(
                        text
                    );


                    return {
                        ok: false,
                        status:
                            response.status,
                        data: null,
                        url
                    };
                }


                // ------------------------------------------------
                // JSON
                // ------------------------------------------------

                const text =
                    await response.text();


                let data;


                try {

                    data =
                        JSON.parse(text);

                } catch (error) {

                    console.error(
                        "❌ Resposta não é JSON válido."
                    );

                    console.error(
                        text.slice(
                            0,
                            1000
                        )
                    );


                    return {
                        ok: false,
                        status:
                            response.status,
                        data: null,
                        url
                    };
                }


                return {
                    ok: true,
                    status:
                        response.status,
                    data,
                    url
                };


            } catch (error) {

                retry++;


                console.error(
                    "❌ Erro de rede:",
                    error
                );


                if (
                    retry >
                    MAX_RETRIES
                ) {

                    return {
                        ok: false,
                        status:
                            "ERROR",
                        data: null,
                        url
                    };
                }


                const wait =
                    10000 *
                    retry;


                console.warn(
                    `⏳ Tentando novamente em ${wait / 1000}s`
                );


                await sleep(
                    wait
                );
            }
        }
    }


    // ============================================================
    // BUSCAR UMA QUERY
    // ============================================================

    async function searchQuery(
        query
    ) {

        console.log("");
        console.log(
            "============================================"
        );

        console.log(
            `${query.id} | ${query.name}`
        );

        console.log(
            "============================================"
        );

        console.log(
            query.qs
        );


        const result = {

            id:
                query.id,

            name:
                query.name,

            qs:
                query.qs,

            status:
                null,

            requests:
                0,

            results:
                [],

            completed:
                false,

            error:
                null
        };


        let offset = 0;

        let page = 1;


        while (true) {

            console.log("");
            console.log(
                `📄 ${query.id} | Página ${page}`
            );

            console.log(
                `offset=${offset}`
            );


            const response =
                await request(
                    query.qs,
                    offset
                );


            result.requests++;


            if (
                !response.ok
            ) {

                result.status =
                    response.status;

                result.error =
                    `Falha em offset=${offset}`;

                console.error(
                    `❌ ${query.id} interrompida`
                );

                break;
            }


            result.status =
                response.status;


            const pageResults =
                response.data
                    ?.searchResults ||
                [];


            console.log(
                `📦 ${pageResults.length} resultados`
            );


            if (
                pageResults.length === 0
            ) {

                console.log(
                    "🏁 Nenhum resultado adicional."
                );

                result.completed =
                    true;

                break;
            }


            // ----------------------------------------------------
            // Adicionar resultados
            // ----------------------------------------------------

            for (
                const article
                of pageResults
            ) {

                result.results.push({

                    ...article,

                    _queryId:
                        query.id,

                    _queryName:
                        query.name,

                    _query:
                        query.qs
                });
            }


            // ----------------------------------------------------
            // Se veio menos que 100,
            // chegamos ao final.
            // ----------------------------------------------------

            if (
                pageResults.length <
                SHOW
            ) {

                console.log(
                    "🏁 Última página."
                );

                result.completed =
                    true;

                break;
            }


            // ----------------------------------------------------
            // Próxima página
            // ----------------------------------------------------

            offset +=
                SHOW;

            page++;


            console.log(
                `⏳ Esperando ${
                    DELAY_BETWEEN_REQUESTS / 1000
                }s...`
            );


            await sleep(
                DELAY_BETWEEN_REQUESTS
            );
        }


        console.log("");
        console.log(
            `✅ ${query.id} finalizada`
        );

        console.log(
            `📚 ${result.results.length} resultados`
        );


        return result;
    }


    // ============================================================
    // EXECUTAR QUERIES
    // ============================================================

    for (
        let i = 0;
        i < queries.length;
        i++
    ) {

        const query =
            queries[i];


        console.log("");
        console.log(
            `🔎 INICIANDO ${query.id}`
        );


        try {

            const result =
                await searchQuery(
                    query
                );


            state.queries.push(
                result
            );


            // Atualiza resultados globais
            state.rawResults =
                state.queries.flatMap(
                    q => q.results
                );


            console.log("");
            console.log(
                `📊 Total bruto até agora: ${
                    state.rawResults.length
                }`
            );


        } catch (error) {

            console.error(
                `❌ Erro em ${query.id}`,
                error
            );


            state.queries.push({

                ...query,

                status:
                    "ERROR",

                results:
                    [],

                completed:
                    false,

                error:
                    String(error)
            });
        }


        // --------------------------------------------------------
        // Delay entre QUERIES
        // --------------------------------------------------------

        if (
            i <
            queries.length - 1
        ) {

            console.log("");
            console.log(
                "🛑 Pausa entre consultas..."
            );

            console.log(
                `⏳ ${
                    DELAY_BETWEEN_REQUESTS / 1000
                }s`
            );


            await sleep(
                DELAY_BETWEEN_REQUESTS
            );
        }
    }


    // ============================================================
    // RESUMO DAS QUERIES
    // ============================================================

    console.log("");
    console.log("");
    console.log(
        "============================================"
    );

    console.log(
        "RESUMO"
    );

    console.log(
        "============================================"
    );


    for (
        const result
        of state.queries
    ) {

        console.log(

            `${result.id} | ` +

            `${result.status} | ` +

            `${result.results.length} resultados | ` +

            `${result.completed
                ? "COMPLETA"
                : "INCOMPLETA"} | ` +

            result.name

        );
    }


    console.log("");
    console.log(
        `🌐 Requisições: ${state.totalRequests}`
    );

    console.log(
        `🚦 HTTP 429: ${state.total429}`
    );

    console.log(
        `📚 Resultados brutos: ${
            state.rawResults.length
        }`
    );


    // ============================================================
    // DEDUPLICAÇÃO
    // ============================================================

    function normalizeTitle(
        title
    ) {

        return (
            title || ""
        )
            .toLowerCase()
            .replace(
                /<[^>]*>/g,
                ""
            )
            .replace(
                /[^a-z0-9]+/g,
                " "
            )
            .trim();
    }


    const uniqueMap =
        new Map();


    for (
        const article
        of state.rawResults
    ) {

        const doi =
            (
                article.doi ||
                ""
            )
                .toLowerCase()
                .trim();


        const pii =
            (
                article.pii ||
                ""
            )
                .toLowerCase()
                .trim();


        const title =
            normalizeTitle(
                article.title
            );


        let key;


        if (doi) {

            key =
                `doi:${doi}`;

        } else if (pii) {

            key =
                `pii:${pii}`;

        } else if (title) {

            key =
                `title:${title}`;

        } else {

            key =
                `unknown:${article.cid || Math.random()}`;
        }


        if (
            !uniqueMap.has(key)
        ) {

            uniqueMap.set(
                key,
                {
                    ...article,

                    _foundBy:
                        [
                            article._queryId
                        ]
                }
            );

        } else {

            const existing =
                uniqueMap.get(
                    key
                );


            if (
                !existing._foundBy.includes(
                    article._queryId
                )
            ) {

                existing._foundBy.push(
                    article._queryId
                );
            }
        }
    }


    state.uniqueResults =
        Array.from(
            uniqueMap.values()
        );


    console.log("");
    console.log(
        "============================================"
    );

    console.log(
        `📚 BRUTOS: ${
            state.rawResults.length
        }`
    );

    console.log(
        `🧹 ÚNICOS: ${
            state.uniqueResults.length
        }`
    );

    console.log(
        `♻️ DUPLICADOS: ${
            state.rawResults.length -
            state.uniqueResults.length
        }`
    );

    console.log(
        "============================================"
    );


    // ============================================================
    // JSON
    // ============================================================

    const jsonOutput = {

        source:
            "ScienceDirect",

        generatedAt:
            new Date().toISOString(),

        configuration: {

            show:
                SHOW,

            delayBetweenRequests:
                DELAY_BETWEEN_REQUESTS,

            maxRetries:
                MAX_RETRIES
        },

        summary: {

            queries:
                queries.length,

            requests:
                state.totalRequests,

            rateLimit429:
                state.total429,

            rawResults:
                state.rawResults.length,

            uniqueResults:
                state.uniqueResults.length,

            duplicates:
                state.rawResults.length -
                state.uniqueResults.length
        },

        queries:
            state.queries,

        uniqueResults:
            state.uniqueResults
    };


    // ============================================================
    // DOWNLOAD
    // ============================================================

    function downloadFile(
        content,
        filename,
        type
    ) {

        const blob =
            new Blob(
                [
                    content
                ],
                {
                    type
                }
            );


        const url =
            URL.createObjectURL(
                blob
            );


        const a =
            document.createElement(
                "a"
            );


        a.href =
            url;

        a.download =
            filename;


        document.body.appendChild(
            a
        );


        a.click();


        a.remove();


        setTimeout(
            () => {

                URL.revokeObjectURL(
                    url
                );

            },
            2000
        );
    }


    downloadFile(

        JSON.stringify(
            jsonOutput,
            null,
            2
        ),

        "sciencedirect_prompt_injection.json",

        "application/json;charset=utf-8"
    );


    // ============================================================
    // BIBTEX
    // ============================================================

    function escapeBibtex(
        value
    ) {

        if (
            value === null ||
            value === undefined
        ) {

            return "";
        }


        return String(value)

            .replace(
                /\\/g,
                "\\\\"
            )

            .replace(
                /[{}]/g,
                ""
            )

            .replace(
                /&/g,
                "\\&"
            )

            .replace(
                /%/g,
                "\\%"
            )

            .replace(
                /#/g,
                "\\#"
            )

            .replace(
                /_/g,
                "\\_"
            )

            .replace(
                /\$/g,
                "\\$"
            );
    }


    function getYear(
        article
    ) {

        if (
            article.sortDate
        ) {

            return new Date(
                article.sortDate
            )
                .getFullYear();
        }


        const match =
            (
                article.publicationDateDisplay ||
                ""
            )
                .match(
                    /\d{4}/
                );


        return match
            ? match[0]
            : "";
    }


    function bibKey(
        article,
        index
    ) {

        const author =
            article.authors?.[0]?.name
            || "Unknown";


        const surname =
            author
                .split(/\s+/)
                .pop()
                .replace(
                    /[^a-zA-Z0-9]/g,
                    ""
                );


        const year =
            getYear(
                article
            )
            || "nd";


        const titleWord =
            (
                article.title ||
                "Paper"
            )
                .split(/\s+/)[0]
                .replace(
                    /[^a-zA-Z0-9]/g,
                    ""
                );


        return (
            surname +
            year +
            titleWord +
            index
        );
    }


    function toBibtex(
        article,
        index
    ) {

        const fields = [];


        // --------------------------------------------------------
        // TITLE
        // --------------------------------------------------------

        if (
            article.title
        ) {

            fields.push(
                `  title = {${escapeBibtex(
                    article.title
                )}}`
            );
        }


        // --------------------------------------------------------
        // AUTHORS
        // --------------------------------------------------------

        const authors =
            (
                article.authors ||
                []
            )
                .sort(
                    (a, b) =>
                        (
                            a.order || 0
                        ) -
                        (
                            b.order || 0
                        )
                )
                .map(
                    a =>
                        a.name
                )
                .filter(Boolean)
                .join(
                    " and "
                );


        if (
            authors
        ) {

            fields.push(
                `  author = {${escapeBibtex(
                    authors
                )}}`
            );
        }


        // --------------------------------------------------------
        // JOURNAL
        // --------------------------------------------------------

        if (
            article.sourceTitle
        ) {

            fields.push(
                `  journal = {${escapeBibtex(
                    article.sourceTitle
                )}}`
            );
        }


        // --------------------------------------------------------
        // YEAR
        // --------------------------------------------------------

        const year =
            getYear(
                article
            );


        if (
            year
        ) {

            fields.push(
                `  year = {${year}}`
            );
        }


        // --------------------------------------------------------
        // VOLUME / ISSUE
        // --------------------------------------------------------

        if (
            article.volumeIssue
        ) {

            const volume =
                article.volumeIssue
                    .match(
                        /Volume\s+([^,]+)/i
                    );


            const issue =
                article.volumeIssue
                    .match(
                        /Issue\s+([^,]+)/i
                    );


            if (
                volume
            ) {

                fields.push(
                    `  volume = {${escapeBibtex(
                        volume[1]
                    )}}`
                );
            }


            if (
                issue
            ) {

                fields.push(
                    `  number = {${escapeBibtex(
                        issue[1]
                    )}}`
                );
            }
        }


        // --------------------------------------------------------
        // PAGES
        // --------------------------------------------------------

        if (
            article.pages?.first
        ) {

            fields.push(
                `  pages = {${escapeBibtex(
                    article.pages.first
                )}}`
            );
        }


        // --------------------------------------------------------
        // DOI
        // --------------------------------------------------------

        if (
            article.doi
        ) {

            fields.push(
                `  doi = {${escapeBibtex(
                    article.doi
                )}}`
            );
        }


        // --------------------------------------------------------
        // ISSN
        // --------------------------------------------------------

        if (
            article.issn
        ) {

            fields.push(
                `  issn = {${escapeBibtex(
                    article.issn
                )}}`
            );
        }


        // --------------------------------------------------------
        // URL
        // --------------------------------------------------------

        if (
            article.link
        ) {

            fields.push(
                `  url = {https://www.sciencedirect.com${article.link}}`
            );
        }


        fields.push(
            "  publisher = {Elsevier}"
        );


        const key =
            bibKey(
                article,
                index
            );


        return (
            `@article{${key},\n` +
            fields.join(
                ",\n"
            ) +
            "\n}\n"
        );
    }


    const bibtex =
        state.uniqueResults
            .map(
                (
                    article,
                    index
                ) =>
                    toBibtex(
                        article,
                        index + 1
                    )
            )
            .join(
                "\n"
            );


    downloadFile(

        bibtex,

        "sciencedirect_prompt_injection.bib",

        "application/x-bibtex;charset=utf-8"
    );


    // ============================================================
    // SALVAR NO WINDOW
    // ============================================================

    window.sciencedirectResults = {

        state,

        json:
            JSON.stringify(
                jsonOutput,
                null,
                2
            ),

        bibtex,

        uniqueResults:
            state.uniqueResults,

        rawResults:
            state.rawResults
    };


    // ============================================================
    // FINAL
    // ============================================================

    console.log("");
    console.log("");
    console.log(
        "╔══════════════════════════════════════════╗"
    );

    console.log(
        "║       🎉 COLETA FINALIZADA              ║"
    );

    console.log(
        "╚══════════════════════════════════════════╝"
    );

    console.log("");

    console.log(
        `📚 Resultados brutos: ${
            state.rawResults.length
        }`
    );

    console.log(
        `🧹 Resultados únicos: ${
            state.uniqueResults.length
        }`
    );

    console.log(
        `♻️ Duplicados: ${
            state.rawResults.length -
            state.uniqueResults.length
        }`
    );

    console.log(
        `🌐 Requisições: ${
            state.totalRequests
        }`
    );

    console.log(
        `🚦 HTTP 429: ${
            state.total429
        }`
    );

    console.log("");

    console.log(
        "📥 Arquivos baixados:"
    );

    console.log(
        "   sciencedirect_prompt_injection.json"
    );

    console.log(
        "   sciencedirect_prompt_injection.bib"
    );

    console.log("");

    console.log(
        "📦 Dados disponíveis em:"
    );

    console.log(
        "window.sciencedirectResults"
    );

})();