Link da pesquisa para replicar
https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText=((%0A%20%20%22All%20Metadata%22:%22large%20language%20model*%22%0A%20%20OR%20%22All%20Metadata%22:LLM*%0A%20%20OR%20%22All%20Metadata%22:GPT*%0A%20%20OR%20%22All%20Metadata%22:ChatGPT%0A%20%20OR%20%22All%20Metadata%22:RAG%0A)%0AAND%0A(%0A%20%20%22Document%20Title%22:%22prompt%20inject*%22%0A%20%20OR%20%22Abstract%22:%22prompt%20inject*%22%0A%20%20OR%20%22Document%20Title%22:jailbreak*%0A%20%20OR%20%22Abstract%22:jailbreak*%0A))&returnFacets=ALL&rowsPerPage=100&highlight=true&returnType=SEARCH&matchPubs=true&sortType=newest&ranges=20220101_20260901_Search%20Latest%20Date



https://link.springer.com/search?query=%22large+language+model%22+OR+%22large+language+models%22+OR+LLM*+OR+GPT*+OR+ChatGPT+OR+RAG&advancedSearch=true&title=%22prompt+injection%22+OR+%22prompt+injections%22+OR+%22prompt-injection%22+OR+jailbreak*&date=custom&dateFrom=2022&dateTo=2026&sortBy=relevance&page=1





----

## Estratégia de busca no IEEE Xplore

A busca no IEEE Xplore foi realizada com o objetivo de identificar estudos relacionados a ataques de *prompt injection* e *jailbreak* em sistemas baseados em grandes modelos de linguagem.

### Período de publicação

Foram considerados trabalhos publicados entre **1º de janeiro de 2022 e 1º de setembro de 2026**, inclusive.

A escolha de 2022 como limite inferior busca abranger o período de surgimento da literatura moderna sobre *prompt injection* em grandes modelos de linguagem, mantendo uma margem temporal anterior aos primeiros trabalhos amplamente reconhecidos sobre o fenômeno. O limite superior de 1º de setembro de 2026 estabelece um ponto de corte temporal fixo para a revisão.

Para fins de registro não ambíguo, o intervalo corresponde a:

**2022-01-01 a 2026-09-01.**

### String de busca

```text
(
  "All Metadata":"large language model*"
  OR "All Metadata":LLM*
  OR "All Metadata":GPT*
  OR "All Metadata":ChatGPT
  OR "All Metadata":RAG
)
AND
(
  "Document Title":"prompt inject*"
  OR "Abstract":"prompt inject*"
  OR "Document Title":jailbreak*
  OR "Abstract":jailbreak*
)
```

### Estrutura da estratégia

A string foi organizada em dois blocos conceituais.

O primeiro bloco identifica sistemas e arquiteturas relacionados a grandes modelos de linguagem, utilizando os termos *large language model*, LLM, GPT, ChatGPT e RAG (*Retrieval-Augmented Generation*).

O segundo bloco identifica os fenômenos de segurança de interesse: *prompt injection* e *jailbreak*. Esses termos foram restringidos aos campos de título e resumo, com o objetivo de priorizar estudos em que esses fenômenos constituam parte central do trabalho, em vez de artigos que apenas os mencionem de forma secundária.

Não foram adicionados termos obrigatórios relacionados a ataque, defesa, detecção ou mitigação, uma vez que essa restrição poderia excluir estudos relevantes que empregam terminologias diferentes. A classificação dos trabalhos quanto ao tipo de contribuição será realizada posteriormente durante a etapa de triagem.

Também não foram aplicadas restrições quanto ao tipo de estudo nessa etapa. Assim, podem ser recuperados estudos primários, propostas de ataques e defesas, métodos de detecção, avaliações experimentais, benchmarks, trabalhos de *red teaming*, taxonomias, surveys e revisões da literatura.

### Resultado da busca

A execução da estratégia no IEEE Xplore, com o intervalo de publicação entre **1º de janeiro de 2022 e 1º de setembro de 2026**, recuperou **464 registros**.

Esses 464 registros constituem o conjunto bruto inicial proveniente do IEEE Xplore e serão submetidos posteriormente às etapas de organização, deduplicação e triagem por título e resumo.
----





----


# Metodologia de triagem e priorização de estudos por título e resumo

## 1. Objetivo da etapa

Após a execução das estratégias de busca nas bases bibliográficas, os registros recuperados passam por uma etapa de triagem baseada inicialmente em **título e resumo**.

O objetivo dessa fase não é responder integralmente às perguntas de pesquisa da revisão, nem realizar uma avaliação definitiva da qualidade metodológica dos estudos. Essas atividades serão realizadas posteriormente, durante a leitura do texto completo.

Nesta etapa, o objetivo é estimar o **potencial de relevância de cada estudo para a revisão**, identificando quais trabalhos possuem maior probabilidade de fornecer evidências relacionadas a ataques por *prompt injection*, *jailbreak*, mecanismos de exploração, estratégias de defesa e contextos de aplicação relevantes.

A triagem é realizada de forma independente para cada registro, utilizando critérios previamente definidos e uma escala contínua de relevância.

---

# 2. Separação entre triagem e extração de dados

A revisão é organizada em pelo menos duas fases distintas.

## 2.1. Triagem por título e resumo

Nesta fase são utilizados apenas os metadados disponíveis, principalmente:

* título;
* resumo;
* palavras-chave, quando disponíveis;
* ano;
* tipo de publicação;
* DOI e demais identificadores bibliográficos.

O objetivo é decidir quais estudos possuem prioridade para leitura integral.

Não se busca, nesta etapa, responder detalhadamente questões como:

* qual ataque foi implementado;
* qual dataset foi utilizado;
* qual foi a taxa de sucesso do ataque;
* qual modelo apresentou maior robustez;
* qual técnica de mitigação foi mais eficaz;
* quais limitações metodológicas foram relatadas.

Essas informações exigem acesso ao texto completo e serão extraídas posteriormente.

## 2.2. Análise de texto completo

Somente os estudos selecionados após a triagem serão submetidos à análise integral.

Nessa fase, serão extraídas informações relacionadas às perguntas da revisão, incluindo:

* tipos de ataques;
* vetores de entrada;
* mecanismos de exploração;
* objetivos dos atacantes;
* estratégias de prevenção;
* estratégias de detecção;
* estratégias de mitigação;
* mecanismos de defesa;
* tarefas e contextos de aplicação;
* modelos utilizados;
* datasets;
* métricas;
* protocolos experimentais;
* limitações;
* lacunas de pesquisa.

---

# 3. Uso de uma pontuação contínua de relevância

Em vez de classificar os estudos apenas como `incluir` ou `excluir`, cada registro recebe uma pontuação contínua denominada:

```text
relevance_score
```

A pontuação varia entre:

```text
0.00 e 1.00
```

Quanto maior a pontuação, maior o potencial estimado de o estudo contribuir para as perguntas da revisão.

Essa abordagem foi escolhida porque permite separar dois processos diferentes:

1. **avaliação da relevância do artigo**;
2. **definição posterior do ponto de corte para leitura integral**.

Dessa forma, a escala de avaliação permanece fixa durante toda a revisão, enquanto o limite utilizado para selecionar estudos pode ser ajustado posteriormente de acordo com:

* quantidade total de trabalhos recuperados;
* quantidade de estudos altamente relevantes;
* recursos disponíveis para leitura completa;
* distribuição das pontuações;
* necessidade de aumentar ou diminuir a sensibilidade da seleção.

Por exemplo, caso poucos estudos apresentem pontuação elevada, o ponto de corte pode ser reduzido sem necessidade de reavaliar os registros.

Da mesma forma, caso centenas de estudos apresentem alta relevância, o ponto de corte pode ser elevado.

---

# 4. Princípio de independência da avaliação

Cada artigo deve ser avaliado **independentemente dos demais**.

A pontuação atribuída a um registro não deve depender:

* da base bibliográfica de origem;
* da posição do artigo nos resultados da busca;
* da quantidade de artigos existentes no mesmo lote;
* da qualidade relativa dos demais artigos;
* da quantidade desejada de trabalhos ao final da revisão.

Por exemplo, um artigo avaliado com pontuação `0.82` no IEEE Xplore deve receber aproximadamente a mesma pontuação caso apareça posteriormente na ACM Digital Library ou Springer, considerando os mesmos título e resumo.

O modelo de triagem não deve utilizar um raciocínio como:

> Este é o melhor artigo do lote, portanto deve receber pontuação alta.

O raciocínio esperado é:

> Considerando exclusivamente os critérios previamente definidos, este artigo apresenta estas características e, portanto, recebe determinada pontuação.

Isso permite combinar registros provenientes de diferentes bases sem alterar a interpretação da escala.

---

# 5. Dimensões da pontuação de relevância

A pontuação final é calculada a partir de cinco dimensões.

Cada dimensão recebe um valor entre:

```text
0.00
0.25
0.50
0.75
1.00
```

Valores intermediários podem ser utilizados quando necessário, desde que preservada a interpretação da escala.

As cinco dimensões são:

| Critério                                       | Peso |
| ---------------------------------------------- | ---: |
| R1 — Centralidade do fenômeno                  | 0.35 |
| R2 — Contribuição para as perguntas da revisão | 0.25 |
| R3 — Contexto de aplicação                     | 0.15 |
| R4 — Evidência empírica ou síntese             | 0.15 |
| R5 — Densidade informacional do resumo         | 0.10 |

A pontuação final é calculada por:

```text
relevance_score =
    0.35 × R1
  + 0.25 × R2
  + 0.15 × R3
  + 0.15 × R4
  + 0.10 × R5
```

A soma dos pesos é igual a:

```text
1.00
```

---

# 6. R1 — Centralidade do fenômeno

**Peso: 35%**

Esse critério avalia o quanto *prompt injection*, *jailbreak* ou ataques diretamente relacionados constituem o objeto central do trabalho.

Essa é a dimensão de maior peso, uma vez que a revisão tem como foco principal esses mecanismos de ataque e suas respectivas estratégias de mitigação.

Sugestão de interpretação:

| Pontuação | Interpretação                                                        |
| --------: | -------------------------------------------------------------------- |
|      1.00 | Prompt injection/jailbreak é o fenômeno principal do estudo          |
|      0.75 | É um dos temas principais do trabalho                                |
|      0.50 | O fenômeno é relevante, mas divide espaço com diversos outros riscos |
|      0.25 | É mencionado apenas como ameaça ou aspecto secundário                |
|      0.00 | O estudo não trata efetivamente do fenômeno de interesse             |

Também recebe pontuação baixa ou nula o trabalho que utiliza o termo *prompt injection* com significado diferente do ataque de segurança investigado na revisão.

Por exemplo, expressões como:

```text
dynamic prompt injection
```

podem eventualmente representar apenas uma técnica de composição dinâmica de prompts e não uma exploração adversarial.

---

# 7. R2 — Contribuição potencial para as perguntas de pesquisa

**Peso: 25%**

Esse critério avalia se o estudo parece fornecer informações que poderão contribuir diretamente para as perguntas da revisão durante a leitura integral.

São consideradas contribuições relevantes, entre outras:

* nova técnica de ataque;
* novo mecanismo de exploração;
* nova técnica de jailbreak;
* estudo de *indirect prompt injection*;
* método de detecção;
* estratégia preventiva;
* estratégia de mitigação;
* mecanismo de defesa;
* técnica de filtragem;
* *red teaming*;
* framework de geração de ataques;
* benchmark;
* avaliação comparativa;
* taxonomia;
* survey;
* revisão sistemática;
* revisão de escopo;
* análise estruturada de vulnerabilidades.

Sugestão de interpretação:

| Pontuação | Interpretação                                                           |
| --------: | ----------------------------------------------------------------------- |
|      1.00 | Contribuição diretamente relacionada a uma ou mais perguntas da revisão |
|      0.75 | Contribuição claramente relevante, embora parcial                       |
|      0.50 | Discussão relacionada, mas contribuição pouco definida                  |
|      0.25 | Relação indireta ou superficial                                         |
|      0.00 | Não apresenta contribuição relevante para as perguntas da revisão       |

Tanto estudos primários quanto secundários podem receber pontuação máxima.

---

# 8. R3 — Contexto de aplicação

**Peso: 15%**

Esse critério avalia o quanto o contexto no qual o ataque ou defesa é estudado se aproxima das aplicações de interesse da revisão.

O foco original da investigação envolve sistemas de Reconhecimento de Entidades Nomeadas e tarefas relacionadas à extração de informações, porém a revisão também considera evidências mais gerais que possam ser transferidas para esses contextos.

Uma escala indicativa pode ser utilizada:

| Pontuação aproximada | Contexto                                                                                   |
| -------------------: | ------------------------------------------------------------------------------------------ |
|                 1.00 | NER, named entity recognition, named entity extraction ou extração diretamente relacionada |
|                 0.90 | Information Extraction, processamento documental ou document understanding                 |
|                 0.90 | RAG processando conteúdo externo potencialmente não confiável                              |
|                 0.75 | Agentes, websites, e-mails, ferramentas externas, sistemas multimodais ou documentos       |
|                 0.50 | Segurança geral de aplicações baseadas em LLM                                              |
|                 0.25 | Contexto muito específico e pouco transferível                                             |
|                 0.00 | Sem relação útil com aplicações de interesse                                               |

O contexto de NER não é utilizado como requisito obrigatório.

Dessa forma, um estudo altamente relevante sobre jailbreak em LLMs pode continuar recebendo pontuação elevada mesmo sem investigar diretamente uma aplicação de reconhecimento de entidades.

---

# 9. R4 — Evidência empírica ou síntese estruturada

**Peso: 15%**

Esse critério estima, a partir do resumo, se o estudo apresenta material empírico ou uma síntese suficientemente estruturada para contribuir com a revisão.

Nesta etapa não se avalia ainda a qualidade metodológica profunda do experimento.

O objetivo é apenas identificar a presença de elementos como:

* experimentos;
* benchmarks;
* múltiplos modelos avaliados;
* datasets;
* métricas;
* Attack Success Rate;
* comparações entre ataques;
* comparações entre defesas;
* estudos de ablação;
* avaliações quantitativas;
* avaliações qualitativas estruturadas;
* revisões sistemáticas;
* surveys;
* taxonomias.

Sugestão:

| Pontuação | Interpretação                                                         |
| --------: | --------------------------------------------------------------------- |
|      1.00 | Evidência experimental substancial ou revisão sistemática estruturada |
|      0.75 | Benchmark, survey, taxonomia ou avaliação relevante                   |
|      0.50 | Evidência presente, porém limitada                                    |
|      0.25 | Discussão predominantemente conceitual                                |
|      0.00 | Ausência de evidência ou síntese identificável                        |

Uma revisão sistemática pode receber pontuação alta nesse critério mesmo sem realizar experimentos próprios.

---

# 10. R5 — Densidade informacional do resumo

**Peso: 10%**

Esse critério avalia a quantidade de informação útil presente no título e no resumo.

Um resumo informativo tende a apresentar elementos como:

* problema investigado;
* técnica proposta;
* tipo de ataque;
* modelo avaliado;
* dataset;
* métrica;
* mecanismo de defesa;
* resultado experimental;
* contexto de aplicação.

Exemplo de alta densidade:

> O estudo propõe um novo ataque de jailbreak, avalia três LLMs em determinado benchmark e compara a taxa de sucesso contra duas estratégias de defesa.

Esse tipo de resumo receberia pontuação próxima de `1.00`.

Por outro lado, um resumo genérico como:

> Este trabalho discute desafios de segurança em modelos de linguagem e possíveis abordagens futuras.

receberia pontuação mais baixa.

Sugestão:

| Pontuação | Interpretação                                                     |
| --------: | ----------------------------------------------------------------- |
|      1.00 | Abstract muito informativo e específico                           |
|      0.75 | Informações suficientes para compreender contribuição e avaliação |
|      0.50 | Informações parciais                                              |
|      0.25 | Abstract genérico                                                 |
|      0.00 | Informações insuficientes                                         |

---

# 11. Exclusão direta

Antes da aplicação completa da pontuação, pode ser utilizado um indicador de exclusão direta:

```text
hard_exclude
```

Essa variável é booleana:

```text
true
false
```

A exclusão direta deve ser utilizada de maneira conservadora.

Um registro pode receber:

```json
"hard_exclude": true
```

quando título e resumo permitem concluir com alto grau de confiança que o trabalho:

* não é relacionado a modelos de linguagem ou sistemas equivalentes;
* não trata de prompt injection, jailbreak ou mecanismo relacionado como problema de segurança;
* utiliza o termo *prompt injection* com significado completamente diferente;
* está claramente fora do escopo definido;
* é um falso positivo evidente da estratégia de busca.

Quando `hard_exclude = true`, a pontuação de relevância pode ser definida como:

```text
0.00
```

A ausência de informações suficientes no resumo **não deve ser considerada motivo para exclusão direta**.

Nesses casos, o estudo deve permanecer como incerto, com redução na confiança da avaliação.

---

# 12. Separação entre relevância e confiança

Além da pontuação de relevância, cada avaliação recebe uma segunda variável:

```text
confidence
```

Também variando entre:

```text
0.00 e 1.00
```

A variável `confidence` representa o grau de segurança da classificação realizada com base no título e resumo.

Ela não altera o `relevance_score`.

Exemplo:

```json
{
  "relevance_score": 0.88,
  "confidence": 0.96
}
```

indica que o artigo parece altamente relevante e que o resumo fornece evidências claras para essa conclusão.

Outro exemplo:

```json
{
  "relevance_score": 0.63,
  "confidence": 0.42
}
```

indica relevância potencial moderada, porém com informações insuficientes no resumo para uma avaliação segura.

Estudos com baixa confiança podem ser priorizados para revisão manual independentemente de sua pontuação.

---

# 13. Classificação do tipo de estudo

Durante a triagem, cada artigo também pode receber uma classificação preliminar referente ao tipo de contribuição.

Categorias propostas:

```text
PRIMARY_ATTACK
PRIMARY_DEFENSE
PRIMARY_ATTACK_AND_DEFENSE
DETECTION
RED_TEAMING
BENCHMARK_EVALUATION
REVIEW
SURVEY
TAXONOMY
APPLICATION_SECURITY
OTHER
```

Essas categorias não interferem diretamente na pontuação.

Seu objetivo é permitir a caracterização posterior do conjunto de estudos.

Um estudo também pode possuir múltiplos tipos de contribuição, armazenados separadamente, por exemplo:

```json
"contribution_types": [
  "ATTACK",
  "DEFENSE",
  "EVALUATION"
]
```

---

# 14. Estrutura de saída da triagem

A avaliação de cada registro pode ser armazenada em JSON utilizando a seguinte estrutura:

```json
{
  "id": "IEEE_0001",
  "title": "Example title",

  "relevance_score": 0.87,
  "confidence": 0.94,

  "scores": {
    "phenomenon_centrality": 1.00,
    "rq_contribution": 1.00,
    "application_context": 0.50,
    "evidence_or_synthesis": 0.75,
    "information_density": 0.75
  },

  "hard_exclude": false,

  "study_type": "PRIMARY_ATTACK",

  "contribution_types": [
    "ATTACK",
    "EVALUATION"
  ],

  "contexts": [
    "GENERAL_LLM"
  ],

  "reason": "Propõe e avalia diretamente uma técnica de jailbreak em diferentes modelos, apresentando evidências experimentais relevantes para a caracterização de vetores de ataque."
}
```

O campo `reason` deve conter uma justificativa curta e objetiva para a classificação.

---

# 15. Processamento em lotes

Como as buscas podem recuperar centenas ou milhares de registros, a triagem pode ser realizada em lotes.

Fluxo proposto:

```text
Resultados bibliográficos
        ↓
BibTeX / RIS / CSV
        ↓
normalização dos registros
        ↓
JSONL
        ↓
divisão em lotes
        ↓
avaliação automática
        ↓
validação estrutural
        ↓
combinação dos resultados
        ↓
análise da distribuição das pontuações
```

Um tamanho de lote entre aproximadamente:

```text
30 e 50 artigos
```

é considerado adequado para manter consistência, reduzir erros estruturais e facilitar eventuais reprocessamentos.

Todos os lotes devem utilizar:

* o mesmo prompt;
* a mesma rubrica;
* os mesmos pesos;
* o mesmo formato de saída;
* as mesmas instruções.

---

# 16. Instrução de independência para avaliação automatizada

O sistema utilizado na triagem deve receber explicitamente uma instrução semelhante a:

> Avalie cada artigo de forma independente. Não compare um artigo com os demais registros do lote. A pontuação deve refletir exclusivamente o grau de aderência do artigo aos critérios definidos. Não ajuste a escala com base na quantidade ou qualidade dos outros estudos apresentados.

Essa instrução busca minimizar variações decorrentes da composição de cada lote.

---

# 17. Definição posterior do ponto de corte

O ponto de corte para leitura integral não precisa ser definido antes da classificação.

Após a avaliação de todos os registros das diferentes bases, pode-se analisar a distribuição dos valores de `relevance_score`.

Exemplo hipotético:

| Faixa     | Quantidade |
| --------- | ---------: |
| 0.90–1.00 |         27 |
| 0.80–0.89 |         46 |
| 0.70–0.79 |         71 |
| 0.60–0.69 |        103 |
| 0.50–0.59 |        128 |
| < 0.50    |        350 |

A partir dessa distribuição, pode ser definido um limite compatível com a capacidade de leitura integral.

Por exemplo:

```text
relevance_score >= 0.80
```

poderia ser utilizado caso se deseje selecionar aproximadamente os estudos de maior prioridade.

Caso poucos estudos atinjam esse limite, ele pode ser reduzido.

A alteração do ponto de corte não exige reavaliação dos artigos, pois a rubrica permanece constante.

---

# 18. Faixas interpretativas preliminares

Para facilitar a análise exploratória, podem ser utilizadas faixas de prioridade.

Esses intervalos não constituem critérios definitivos de inclusão.

| Score     | Interpretação       |
| --------- | ------------------- |
| 0.80–1.00 | Alta prioridade     |
| 0.65–0.79 | Provável relevância |
| 0.50–0.64 | Zona cinzenta       |
| 0.25–0.49 | Baixa prioridade    |
| 0.00–0.24 | Provável exclusão   |

A seleção final deverá ser baseada na distribuição global dos resultados e nos critérios metodológicos estabelecidos.

---

# 19. Tratamento da zona cinzenta

Artigos próximos ao ponto de corte devem receber atenção especial.

Essa região pode incluir:

* estudos com abstracts pouco informativos;
* trabalhos com relevância indireta;
* artigos sobre mecanismos semelhantes a prompt injection;
* aplicações incomuns;
* estudos recentes com terminologia ainda não consolidada.

Quando necessário, esses registros podem ser encaminhados para:

* revisão manual;
* leitura parcial do texto completo;
* nova avaliação;
* desempate por um segundo avaliador.

A variável `confidence` pode auxiliar nessa decisão.

---

# 20. Integração entre diferentes bases

Todos os estudos provenientes de diferentes bases devem utilizar exatamente a mesma rubrica.

Por exemplo:

```text
IEEE Xplore
ACM Digital Library
SpringerLink
Scopus
Web of Science
outras fontes
```

A base de origem não deve influenciar a nota.

Após a combinação das bases, devem ser executadas etapas de:

1. normalização dos metadados;
2. identificação de DOI;
3. normalização de títulos;
4. deduplicação;
5. consolidação da origem dos registros;
6. triagem.

Quando o mesmo artigo for recuperado por diferentes bases, deve permanecer apenas um registro principal, mantendo-se a informação das fontes que o recuperaram.

Exemplo:

```json
{
  "sources": [
    "IEEE",
    "Scopus"
  ]
}
```

---

# 21. Justificativa para não responder às perguntas de pesquisa nesta fase

As perguntas da revisão exigem informações frequentemente ausentes dos abstracts.

Entre elas:

* detalhes técnicos do ataque;
* mecanismos internos de exploração;
* configuração experimental;
* prompts utilizados;
* modelos e versões;
* datasets completos;
* métricas;
* baselines;
* resultados quantitativos;
* limitações;
* ameaças à validade.

Tentar extrair essas informações apenas a partir dos abstracts poderia gerar dados incompletos ou inferências não suportadas pelos estudos.

Por essa razão, a etapa de título e resumo limita-se à **priorização de relevância**.

A extração sistemática das respostas às perguntas da revisão será realizada posteriormente utilizando os PDFs integrais dos artigos selecionados.

---

# 22. Relação entre a triagem e as perguntas da revisão

Embora as perguntas de pesquisa não sejam respondidas diretamente nessa fase, a rubrica foi construída para identificar trabalhos com maior probabilidade de fornecer evidências para elas.

As dimensões possuem a seguinte relação geral:

```text
R1 → o estudo realmente trata dos ataques relevantes?

R2 → provavelmente responde alguma das perguntas da revisão?

R3 → o contexto é aplicável a NER, IE, documentos ou RAG?

R4 → há evidência experimental ou síntese utilizável?

R5 → o abstract permite estimar essa relevância com informação suficiente?
```

Dessa forma, a classificação funciona como uma etapa intermediária entre a recuperação bibliográfica e a análise integral dos estudos.

---

# 23. Princípio geral da metodologia

O processo pode ser resumido como:

```text
BUSCA
  ↓
conjunto amplo de estudos
  ↓
DEDUPLICAÇÃO
  ↓
TRIAGEM POR TÍTULO + ABSTRACT
  ↓
relevance_score + confidence
  ↓
análise da distribuição
  ↓
definição do ponto de corte
  ↓
seleção para texto completo
  ↓
ANÁLISE DOS PDFs
  ↓
extração das evidências
  ↓
síntese das respostas às perguntas de pesquisa
```

O objetivo é preservar alta sensibilidade durante a busca bibliográfica e transferir a redução do conjunto de estudos para uma etapa estruturada, auditável e reproduzível de triagem.


---- 

## Estratégia de busca na Springer Nature Link

A busca na Springer Nature Link foi adaptada às limitações e aos campos disponibilizados pela interface da base.

Diferentemente do IEEE Xplore, a Springer não disponibilizou um campo específico para restringir os termos ao resumo. Além disso, o filtro temporal permitiu selecionar apenas anos completos.

### Período de publicação

Foram considerados trabalhos publicados entre:

**2022 e 2026.**

O protocolo geral da revisão estabelece como período de interesse:

**2022-01-01 a 2026-09-01.**

Entretanto, como a interface da Springer permitiu apenas a seleção por ano, o filtro foi configurado para **2022–2026**. Trabalhos publicados após 1º de setembro de 2026 deverão ser identificados e excluídos posteriormente durante a organização ou triagem dos registros.

### Configuração da busca

No campo **Keywords**, foram utilizados os termos relacionados aos modelos e arquiteturas:

```text
"large language model"
OR "large language models"
OR LLM*
OR GPT*
OR ChatGPT
OR RAG
```

No campo **Title**, foram utilizados os termos relacionados aos fenômenos de segurança investigados:

```text
"prompt injection"
OR "prompt injections"
OR "prompt-injection"
OR jailbreak*
```

### Estrutura conceitual

A estratégia pode ser representada como:

```text
LLM / GPT / ChatGPT / RAG
            AND
Prompt Injection / Jailbreak
            ↓
termos de ataque restritos ao título
```

Os termos relacionados a LLMs foram pesquisados no campo de palavras-chave disponibilizado pela Springer, enquanto os termos relacionados a *prompt injection* e *jailbreak* foram restringidos ao título.

Essa adaptação foi utilizada para aumentar a precisão da busca, uma vez que o mecanismo de palavras-chave da Springer também pode recuperar ocorrências presentes no conteúdo indexado do documento.

### Resultado

A execução da busca, com filtro de publicação entre **2022 e 2026**, recuperou:

**91 registros.**

Esses registros serão posteriormente exportados, normalizados, deduplicados e submetidos ao mesmo protocolo de triagem por título e resumo utilizado nas demais bases.


-----