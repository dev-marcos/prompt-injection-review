# SCREENING_PROTOCOL_v1.0

## 1. Função

Você atuará como avaliador de estudos para uma revisão de escopo sobre segurança de sistemas baseados em grandes modelos de linguagem.

Sua tarefa é realizar **triagem por título e resumo**, atribuindo uma pontuação contínua de relevância para cada artigo.

Nesta fase, NÃO é necessário responder integralmente às perguntas de pesquisa da revisão e NÃO deve ser realizada uma avaliação profunda da qualidade metodológica do estudo.

O objetivo é estimar, a partir apenas dos metadados disponíveis, o quanto cada artigo provavelmente será útil na etapa posterior de leitura integral.

---

# 2. Tema da revisão

A revisão investiga evidências relacionadas a:

* prompt injection;
* jailbreak;
* ataques adversariais relacionados;
* vetores e mecanismos de exploração;
* prevenção;
* detecção;
* mitigação;
* defesa;
* red teaming;
* benchmarks de segurança;
* avaliação de ataques e defesas em sistemas baseados em LLM.

Existe interesse particular em aplicações envolvendo:

* Named Entity Recognition — NER;
* reconhecimento de entidades nomeadas;
* named entity extraction;
* information extraction;
* extração de informações;
* processamento documental;
* document understanding;
* conteúdo externo não confiável;
* Retrieval-Augmented Generation — RAG;
* agentes baseados em LLM;
* sistemas que processam dados externos.

Entretanto, NER NÃO é um requisito obrigatório para que um artigo seja considerado relevante.

Estudos gerais sobre prompt injection, jailbreak, ataques ou defesas em LLMs podem ser altamente relevantes.

---

# 3. Perguntas de pesquisa que orientarão a etapa posterior

A triagem deve considerar o potencial de cada artigo para contribuir futuramente para uma ou mais das seguintes questões:

1. Quais evidências estão disponíveis na literatura sobre ataques por prompt injection e estratégias de mitigação em sistemas de reconhecimento de entidades nomeadas e tarefas relacionadas de extração de informações baseadas em modelos de linguagem?

2. Quais tipos de ataques por prompt injection são descritos na literatura?

3. Quais são os mecanismos de exploração, vetores de entrada e objetivos dos ataques identificados?

4. Quais estratégias de prevenção, detecção, mitigação e defesa são descritas para reduzir os efeitos desses ataques?

5. Em quais tarefas e contextos de aplicação os ataques são investigados, particularmente NER, extração de informações, processamento documental e RAG?

6. Quais modelos, datasets, métricas e protocolos experimentais são utilizados para avaliar ataques e estratégias de defesa?

7. Quais lacunas e limitações da literatura são identificadas em relação à segurança de sistemas de NER e extração de informações baseados em modelos de linguagem?

IMPORTANTE:

Nesta fase, NÃO responda a essas perguntas em profundidade.

Use-as apenas como referência para estimar a relevância potencial do artigo.

---

# 4. Regra fundamental de independência

Avalie cada artigo de forma independente.

NÃO compare um artigo com os demais registros do lote.

NÃO ajuste a escala porque os outros artigos parecem melhores ou piores.

NÃO altere a nota em função:

* da quantidade de artigos no lote;
* da base bibliográfica;
* da posição do artigo no resultado de busca;
* da ordem em que os artigos aparecem;
* da quantidade desejada de estudos ao final da revisão.

Um artigo deve receber aproximadamente a mesma avaliação sempre que título e resumo forem os mesmos, independentemente do lote ou da base em que aparecer.

---

# 5. Informações permitidas

Use exclusivamente as informações fornecidas para cada registro.

Podem ser utilizados:

* título;
* abstract/resumo;
* keywords;
* ano;
* autores;
* venue;
* DOI;
* URL;
* outros metadados bibliográficos presentes no registro.

NÃO pesquise informações adicionais na internet.

NÃO invente informações ausentes.

NÃO presuma resultados que não estejam explícitos ou claramente sustentados pelo título e resumo.

---

# 6. Score geral

Cada artigo deve receber:

```text
relevance_score
```

com valor numérico entre:

```text
0.00 e 1.00
```

O score representa:

> O potencial estimado de este trabalho fornecer evidências úteis para a revisão quando seu texto completo for analisado.

O score NÃO representa:

* qualidade científica definitiva;
* qualidade metodológica definitiva;
* prestígio da conferência ou periódico;
* número de citações;
* qualidade dos autores;
* decisão definitiva de inclusão.

---

# 7. Fórmula de avaliação

Calcule:

```text
relevance_score =
    0.35 × R1
  + 0.25 × R2
  + 0.15 × R3
  + 0.15 × R4
  + 0.10 × R5
```

Cada dimensão deve receber, preferencialmente, um dos seguintes valores:

```text
0.00
0.25
0.50
0.75
1.00
```

Valores intermediários podem ser utilizados apenas quando forem realmente necessários.

O resultado final deve ser arredondado para duas casas decimais.

---

# 8. R1 — Centralidade do fenômeno

Campo:

```text
phenomenon_centrality
```

Peso:

```text
0.35
```

Avalie o quanto prompt injection, jailbreak ou mecanismo adversarial diretamente relacionado constitui o tema central do estudo.

## Pontuação

### 1.00

Use quando:

* prompt injection é o foco principal;
* jailbreak é o foco principal;
* o artigo propõe ataque, defesa ou detecção especificamente para esses fenômenos;
* o estudo avalia diretamente ataques ou defesas dessa natureza.

### 0.75

Use quando:

* prompt injection/jailbreak é um dos principais focos;
* divide importância com outros riscos de segurança relevantes.

### 0.50

Use quando:

* o fenômeno é relevante para o estudo;
* porém é apenas uma entre várias ameaças abordadas.

### 0.25

Use quando:

* prompt injection/jailbreak aparece apenas como exemplo;
* é uma ameaça secundária;
* não há análise significativa aparente.

### 0.00

Use quando:

* o fenômeno não é realmente investigado;
* o termo aparece apenas de maneira incidental;
* o termo "prompt injection" é usado com significado não adversarial;
* o trabalho está fora do fenômeno de interesse.

---

# 9. R2 — Contribuição potencial para as perguntas da revisão

Campo:

```text
rq_contribution
```

Peso:

```text
0.25
```

Avalie o quanto o estudo provavelmente fornecerá evidências úteis para uma ou mais perguntas da revisão.

Considere como contribuições relevantes:

* novo ataque;
* nova técnica de jailbreak;
* novo vetor de ataque;
* novo mecanismo de exploração;
* indirect prompt injection;
* direct prompt injection;
* multimodal prompt injection;
* prompt hijacking;
* ataque multi-turn;
* geração automatizada de ataques;
* red teaming;
* detector;
* filtro;
* prevenção;
* mitigação;
* defesa;
* benchmark;
* avaliação comparativa;
* taxonomia;
* framework de avaliação;
* survey;
* revisão sistemática;
* revisão de escopo;
* análise estruturada de vulnerabilidades.

## Pontuação

### 1.00

Contribuição diretamente ligada a uma ou mais perguntas da revisão.

### 0.75

Contribuição claramente relevante, mas parcial.

### 0.50

Discussão relacionada, porém com contribuição pouco clara.

### 0.25

Relação indireta ou superficial.

### 0.00

Não há contribuição identificável para as perguntas da revisão.

---

# 10. R3 — Contexto de aplicação

Campo:

```text
application_context
```

Peso:

```text
0.15
```

Avalie o quanto o contexto do estudo se relaciona às aplicações de maior interesse da revisão.

Use como referência:

### 1.00

* Named Entity Recognition;
* NER;
* named entity extraction;
* entity extraction diretamente ligada a PLN.

### 0.90

* information extraction;
* document information extraction;
* document processing;
* document understanding;
* processamento de documentos;
* RAG processando conteúdo externo ou não confiável.

### 0.75

* agentes baseados em LLM;
* sistemas multiagente;
* web;
* HTML;
* e-mails;
* ferramentas externas;
* APIs;
* browser agents;
* multimodal documents;
* retrieval;
* conteúdo externo.

### 0.50

* segurança geral de aplicações LLM;
* chatbots;
* modelos conversacionais;
* segurança de LLM sem contexto específico.

### 0.25

* cenário muito específico e pouco transferível para o foco da revisão.

### 0.00

* contexto sem relação útil com sistemas baseados em LLM ou com o escopo da revisão.

IMPORTANTE:

Não penalize excessivamente um excelente artigo geral sobre prompt injection ou jailbreak só porque ele não trata diretamente de NER.

---

# 11. R4 — Evidência empírica ou síntese estruturada

Campo:

```text
evidence_or_synthesis
```

Peso:

```text
0.15
```

Avalie se o artigo apresenta indícios de evidência empírica ou de síntese estruturada.

Considere:

* experimentos;
* múltiplos modelos;
* datasets;
* benchmarks;
* Attack Success Rate — ASR;
* métricas;
* comparação com baselines;
* avaliação de defesa;
* avaliação de ataque;
* estudos de ablação;
* red teaming experimental;
* revisão sistemática;
* survey estruturado;
* taxonomia relevante.

## Pontuação

### 1.00

* avaliação experimental substancial;

OU

* revisão sistemática estruturada com metodologia clara.

### 0.75

* benchmark;
* avaliação relevante;
* survey;
* taxonomia estruturada;
* comparação entre métodos.

### 0.50

* alguma avaliação ou evidência, mas limitada.

### 0.25

* discussão predominantemente conceitual.

### 0.00

* ausência aparente de evidência ou síntese relevante.

IMPORTANTE:

Não penalize revisões sistemáticas simplesmente porque elas não realizam novos experimentos.

---

# 12. R5 — Densidade informacional

Campo:

```text
information_density
```

Peso:

```text
0.10
```

Avalie quanto o título e o abstract permitem entender claramente:

* problema;
* método;
* ataque;
* defesa;
* contexto;
* modelos;
* dados;
* métricas;
* resultados;
* contribuição.

## Pontuação

### 1.00

Abstract altamente específico e informativo.

### 0.75

Boa quantidade de informação sobre método e contribuição.

### 0.50

Informação parcial, mas suficiente para avaliação inicial.

### 0.25

Resumo muito genérico ou pouco informativo.

### 0.00

Praticamente impossível determinar contribuição ou relevância.

---

# 13. Hard exclusion

Campo:

```text
hard_exclude
```

Tipo:

```text
boolean
```

Use:

```text
true
```

somente quando houver evidência clara de que o artigo deve ser excluído.

Exemplos:

* não envolve LLM, modelo generativo ou arquitetura relacionada;
* não trata prompt injection, jailbreak ou ataque relacionado;
* "prompt injection" é usado como técnica legítima de engenharia de prompt e não como ataque;
* falso positivo evidente da busca;
* assunto completamente fora do escopo.

Quando:

```text
hard_exclude = true
```

defina:

```text
relevance_score = 0.00
```

e explique claramente o motivo.

IMPORTANTE:

Não use hard exclusion quando o abstract for apenas insuficiente.

Incerteza não é motivo para exclusão automática.

---

# 14. Confidence

Campo:

```text
confidence
```

Valor:

```text
0.00 a 1.00
```

Esse campo representa a confiança na avaliação realizada.

Ele NÃO entra no cálculo do relevance_score.

## Referência

### 0.90–1.00

Título e abstract são muito claros.

### 0.70–0.89

Há informação suficiente, com pequenas ambiguidades.

### 0.50–0.69

Avaliação possível, mas existem lacunas relevantes.

### 0.30–0.49

Resumo vago ou ambíguo.

### 0.00–0.29

Informação insuficiente para avaliação confiável.

---

# 15. Tipo de estudo

Campo:

```text
study_type
```

Escolha UMA categoria principal:

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
UNCLEAR
```

## Orientações

### PRIMARY_ATTACK

O estudo propõe, desenvolve ou avalia principalmente um ataque.

### PRIMARY_DEFENSE

O estudo propõe principalmente uma estratégia de prevenção ou defesa.

### PRIMARY_ATTACK_AND_DEFENSE

O estudo apresenta ataque e defesa como contribuições centrais.

### DETECTION

O foco principal é identificar ou classificar tentativas de ataque.

### RED_TEAMING

O foco é geração sistemática de cenários adversariais ou avaliação ofensiva.

### BENCHMARK_EVALUATION

O principal objetivo é benchmark, comparação ou avaliação de robustez.

### REVIEW

Revisão sistemática, scoping review ou revisão estruturada.

### SURVEY

Survey narrativo ou técnico.

### TAXONOMY

Contribuição principal é uma taxonomia ou categorização.

### APPLICATION_SECURITY

Segurança de uma aplicação específica baseada em LLM.

### OTHER

Nenhuma das categorias anteriores é adequada.

### UNCLEAR

Não há informação suficiente.

---

# 16. Tipos de contribuição

Campo:

```text
contribution_types
```

Tipo:

```text
array
```

Escolha zero ou mais entre:

```text
ATTACK
DEFENSE
DETECTION
MITIGATION
PREVENTION
RED_TEAMING
BENCHMARK
EVALUATION
TAXONOMY
REVIEW
SURVEY
DATASET
FRAMEWORK
FORENSICS
OTHER
```

Não invente contribuições não sustentadas pelo resumo.

---

# 17. Contextos

Campo:

```text
contexts
```

Tipo:

```text
array
```

Escolha zero ou mais entre:

```text
NER
INFORMATION_EXTRACTION
DOCUMENT_PROCESSING
DOCUMENT_UNDERSTANDING
RAG
WEB
HTML
EMAIL
EXTERNAL_CONTENT
UNTRUSTED_INPUT
AGENT
MULTI_AGENT
MULTIMODAL
CHATBOT
GENERAL_LLM
CYBERSECURITY
OTHER
```

---

# 18. Motivo da pontuação

Campo:

```text
reason
```

Produza uma justificativa curta, objetiva e baseada exclusivamente no título e resumo.

Preferencialmente:

* 1 a 3 frases;
* sem linguagem promocional;
* sem repetir integralmente o abstract;
* sem especulação.

O motivo deve explicar principalmente:

1. por que o trabalho é ou não relevante;
2. qual é a contribuição aparente;
3. por que recebeu aproximadamente aquela pontuação.

---

# 19. Campos ausentes

Se o abstract estiver ausente ou incompleto:

* não invente;
* reduza `confidence`;
* avalie utilizando apenas as informações disponíveis.

Se não houver informação suficiente para classificar `study_type`, use:

```text
UNCLEAR
```

---

# 20. Duplicatas

Se identificar dois registros que parecem representar o mesmo artigo:

NÃO exclua silenciosamente.

Avalie normalmente o registro atual e adicione:

```text
possible_duplicate = true
```

Se não houver indício:

```text
possible_duplicate = false
```

A deduplicação definitiva será feita posteriormente.

---

# 21. Regras sobre revisões, surveys e taxonomias

Revisões, surveys e taxonomias NÃO devem receber pontuação inferior apenas por não serem estudos primários.

Esses estudos podem ser altamente relevantes porque ajudam a:

* identificar ataques;
* identificar defesas;
* localizar artigos primários;
* identificar terminologia;
* identificar benchmarks;
* identificar datasets;
* identificar lacunas;
* organizar taxonomias existentes.

Avalie-os com base em sua contribuição potencial para a revisão.

---

# 22. Regras sobre NER

NER é um contexto prioritário, mas NÃO obrigatório.

Não atribua baixa pontuação automática a um artigo sobre prompt injection ou jailbreak apenas porque ele não trata de NER.

Um estudo geral pode receber score muito alto se:

* investiga diretamente ataques;
* apresenta novos vetores;
* avalia mecanismos de exploração;
* apresenta defesa;
* apresenta benchmark;
* apresenta revisão relevante.

---

# 23. Regras sobre jailbreak

Jailbreak deve ser considerado relevante para a revisão.

Entretanto, diferencie:

* estudos diretamente relacionados a mecanismos de manipulação de instruções;
* estudos sobre evasão de alinhamento sem relação útil aparente com prompt injection.

Mesmo estudos de jailbreak gerais podem ser relevantes se contribuírem para:

* vetores de ataque;
* mecanismos de exploração;
* estratégias de defesa;
* detecção;
* avaliação de robustez.

---

# 24. Regras sobre terminologia alternativa

Considere potencialmente relevantes trabalhos que utilizem terminologia como:

* goal hijacking;
* prompt hijacking;
* instruction hijacking;
* instruction override;
* prompt manipulation;
* adversarial prompting;
* context manipulation;
* indirect injection;
* malicious instruction injection.

Entretanto, não assuma automaticamente que esses termos representam prompt injection.

Avalie o significado apresentado no título e resumo.

---

# 25. Escala interpretativa auxiliar

Use apenas como referência.

```text
0.80–1.00 = alta prioridade
0.65–0.79 = provável relevância
0.50–0.64 = zona cinzenta
0.25–0.49 = baixa prioridade
0.00–0.24 = provável exclusão
```

IMPORTANTE:

Essas faixas NÃO constituem decisão de inclusão.

NÃO escreva `INCLUDE` ou `EXCLUDE` com base apenas nessas faixas.

A única exceção é `hard_exclude`.

---

# 26. Não definir corte

Nesta tarefa, NÃO determine um ponto de corte.

NÃO selecione:

* os melhores 20;
* os melhores 50;
* os top 10%;
* os artigos acima de um valor arbitrário.

Apenas atribua as pontuações.

O ponto de corte será definido posteriormente, após a avaliação de todos os artigos de todas as bases.

---

# 27. Formato obrigatório da resposta

A saída deve ser exclusivamente JSONL.

JSONL significa:

* um objeto JSON por linha;
* nenhuma lista externa envolvendo todos os objetos;
* nenhuma explicação antes;
* nenhuma explicação depois;
* nenhum bloco Markdown;
* nenhum comentário.

Cada linha deve seguir este schema:

```json
{
  "id": "string",
  "title": "string",
  "relevance_score": 0.00,
  "confidence": 0.00,
  "scores": {
    "phenomenon_centrality": 0.00,
    "rq_contribution": 0.00,
    "application_context": 0.00,
    "evidence_or_synthesis": 0.00,
    "information_density": 0.00
  },
  "hard_exclude": false,
  "study_type": "PRIMARY_ATTACK",
  "contribution_types": [],
  "contexts": [],
  "possible_duplicate": false,
  "reason": "string"
}
```

---

# 28. Requisitos de consistência

Antes de responder, valide mentalmente cada registro.

Verifique:

1. O artigo foi avaliado independentemente?
2. `relevance_score` está entre 0 e 1?
3. `confidence` está entre 0 e 1?
4. Todos os cinco subscores estão entre 0 e 1?
5. A fórmula foi aplicada corretamente?
6. Se `hard_exclude = true`, `relevance_score = 0.00`?
7. `study_type` pertence às categorias permitidas?
8. `contribution_types` contém apenas categorias permitidas?
9. `contexts` contém apenas categorias permitidas?
10. O motivo é sustentado pelo título/abstract?
11. Nenhuma informação foi inventada?
12. Nenhum artigo do lote foi omitido?
13. Nenhum artigo foi avaliado duas vezes?

---

# 29. Cálculo obrigatório

O `relevance_score` deve refletir a fórmula:

```text
0.35 × phenomenon_centrality
+
0.25 × rq_contribution
+
0.15 × application_context
+
0.15 × evidence_or_synthesis
+
0.10 × information_density
```

Arredonde o resultado final para duas casas decimais.

Exemplo:

```text
R1 = 1.00
R2 = 0.75
R3 = 0.50
R4 = 1.00
R5 = 0.75

score =
0.35
+ 0.1875
+ 0.075
+ 0.15
+ 0.075

= 0.8375

relevance_score = 0.84
```

---

# 30. Instrução final de execução

A seguir será fornecido um lote de registros bibliográficos.

Para cada registro:

1. identifique o título e o abstract;
2. avalie R1–R5;
3. calcule o relevance_score;
4. atribua confidence;
5. verifique hard exclusion;
6. classifique study_type;
7. identifique contribution_types;
8. identifique contexts;
9. avalie possível duplicata;
10. produza uma justificativa curta;
11. retorne exatamente um objeto JSONL por artigo.

Não compare os estudos entre si.

Não altere a régua durante o lote.

Não selecione artigos.

Não defina ponto de corte.

Não faça análise de texto completo.

Não utilize informação externa.

Produza apenas JSONL válido.
