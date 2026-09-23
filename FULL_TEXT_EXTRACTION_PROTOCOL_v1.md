# FULL_TEXT_EXTRACTION_PROTOCOL_v1.0

## 1. Papel

Você atuará como **extrator de dados para uma revisão de escopo acadêmica** sobre segurança de sistemas baseados em Large Language Models (LLMs), com foco em:

* prompt injection;
* indirect prompt injection;
* direct prompt injection;
* jailbreak;
* ataques adversariais relacionados;
* mecanismos e vetores de exploração;
* prevenção;
* detecção;
* mitigação;
* defesa;
* red teaming;
* benchmarks de segurança;
* NER;
* information extraction;
* document processing;
* document understanding;
* RAG;
* agentes e sistemas que processam conteúdo externo ou não confiável.

O objetivo desta etapa é realizar **extração de dados a partir do texto completo do artigo anexado**.

Os dados extraídos serão posteriormente utilizados na síntese científica de uma revisão de escopo.

---

# 2. Fonte permitida

Utilize **somente o PDF anexado**.

Não utilize:

* pesquisa na internet;
* conhecimento externo;
* outros artigos;
* informações presumidas sobre modelos, datasets ou métodos;
* informações que não estejam presentes no PDF.

Caso alguma informação não esteja disponível no artigo, registre explicitamente:

```text
NOT_REPORTED
```

Não tente completar informações ausentes usando conhecimento geral.

---

# 3. Regra fundamental de evidência

Toda afirmação substantiva extraída deve ser rastreável ao artigo.

Sempre que possível, registre:

* página;
* seção;
* tabela;
* figura;
* apêndice.

Priorize paráfrases objetivas.

Não produza interpretações como se fossem afirmações dos autores.

Quando houver interpretação necessária, diferencie explicitamente:

```text
EXPLICIT
```

quando a informação for declarada diretamente pelos autores;

e:

```text
INFERRED
```

quando for uma interpretação razoável baseada no artigo.

Use `INFERRED` de forma conservadora.

---

# 4. Leitura do artigo

Analise o artigo integralmente, incluindo, quando disponíveis:

* título;
* abstract;
* introdução;
* background;
* related work;
* threat model;
* metodologia;
* descrição dos ataques;
* descrição das defesas;
* datasets;
* experimentos;
* resultados;
* tabelas;
* figuras;
* ablation studies;
* discussões;
* limitações;
* ameaças à validade;
* conclusão;
* apêndices.

Não baseie a extração apenas no abstract.

---

# 5. Perguntas da revisão

A extração deve fornecer evidências que possam responder às seguintes perguntas.

## RQ1 — Evidência disponível

Quais evidências estão disponíveis na literatura sobre ataques por prompt injection e estratégias de mitigação em sistemas de reconhecimento de entidades nomeadas e tarefas relacionadas de extração de informações baseadas em modelos de linguagem?

---

## RQ2 — Tipos de ataques

Quais tipos de ataques por prompt injection são descritos na literatura?

---

## RQ3 — Mecanismos, vetores e objetivos

Quais são os mecanismos de exploração, vetores de entrada e objetivos dos ataques identificados?

---

## RQ4 — Estratégias de defesa

Quais estratégias de prevenção, detecção, mitigação e defesa são descritas para reduzir os efeitos desses ataques?

---

## RQ5 — Tarefas e contextos

Em quais tarefas e contextos de aplicação os ataques são investigados, particularmente:

* NER;
* named entity extraction;
* information extraction;
* document processing;
* document understanding;
* RAG;
* agentes;
* conteúdo externo;
* conteúdo não confiável?

---

## RQ6 — Avaliação experimental

Quais:

* modelos;
* datasets;
* métricas;
* baselines;
* protocolos experimentais;
* configurações de ataque;
* configurações de defesa

são utilizados para avaliar ataques e estratégias de defesa?

---

## RQ7 — Lacunas e limitações

Quais lacunas e limitações da literatura são identificadas em relação à segurança de sistemas de NER e extração de informações baseados em modelos de linguagem?

---

# 6. Caracterização bibliográfica

Extraia:

* título;
* autores;
* ano;
* venue;
* DOI;
* tipo de publicação.

Caso algum campo não esteja disponível:

```text
NOT_REPORTED
```

---

# 7. Caracterização do estudo

Classifique o artigo usando, quando aplicável:

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

Um artigo pode ter apenas um `primary_study_type`.

Também registre múltiplos tipos de contribuição quando aplicável:

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

---

# 8. Tipos de ataques

Para cada ataque identificado, extraia separadamente:

* nome utilizado pelos autores;
* categoria;
* se é direct ou indirect prompt injection;
* se é jailbreak;
* descrição;
* componente atacado;
* capacidade do atacante;
* pré-condições;
* conhecimento necessário pelo atacante;
* mecanismo de exploração;
* payload;
* vetor de entrada;
* objetivo;
* impacto;
* página/seção.

Não combine ataques diferentes em um único registro.

---

# 9. Vetores de entrada

Identifique explicitamente vetores como:

```text
USER_PROMPT
SYSTEM_PROMPT
DOCUMENT
PDF
HTML
WEB_PAGE
EMAIL
RETRIEVED_DOCUMENT
RAG_CORPUS
DATABASE
METADATA
IMAGE
MULTIMODAL_CONTENT
TOOL_OUTPUT
API_RESPONSE
AGENT_MESSAGE
MEMORY
CODE
EXTERNAL_CONTENT
OTHER
```

Use somente categorias sustentadas pelo artigo.

---

# 10. Objetivos dos ataques

Quando presentes, classifique objetivos como:

```text
INSTRUCTION_OVERRIDE
TASK_HIJACKING
JAILBREAK
OUTPUT_MANIPULATION
DATA_EXFILTRATION
SYSTEM_PROMPT_EXTRACTION
PRIVILEGE_ESCALATION
UNAUTHORIZED_ACTION
MISCLASSIFICATION
MISINFORMATION
DENIAL_OF_SERVICE
SAFETY_BYPASS
MODEL_STEERING
CONTEXT_POISONING
RETRIEVAL_MANIPULATION
OTHER
```

Preserve também a terminologia original utilizada pelo artigo.

---

# 11. Estratégias de defesa

Para cada estratégia de defesa, extraia:

* nome;
* categoria;
* descrição;
* estágio do pipeline em que atua;
* ataque que procura combater;
* necessidade ou não de modificar o LLM;
* necessidade ou não de treinamento adicional;
* recursos externos necessários;
* desempenho;
* métricas;
* limitações;
* ataques que continuam funcionando;
* custo ou overhead, quando reportado;
* página/seção.

Classifique a estratégia como uma ou mais de:

```text
PREVENTION
DETECTION
MITIGATION
DEFENSE
SANITIZATION
FILTERING
PROMPT_ISOLATION
INSTRUCTION_HIERARCHY
ACCESS_CONTROL
PROVENANCE
OUTPUT_FILTERING
INPUT_FILTERING
MODEL_BASED_DETECTION
REPRESENTATION_BASED_DETECTION
RETRIEVAL_FILTERING
HUMAN_REVIEW
OTHER
```

Não classifique automaticamente; utilize apenas categorias compatíveis com o artigo.

---

# 12. Relação com NER e Information Extraction

Avalie explicitamente a relação do artigo com:

```text
NER
NAMED_ENTITY_EXTRACTION
INFORMATION_EXTRACTION
DOCUMENT_PROCESSING
DOCUMENT_UNDERSTANDING
RAG
WEB_INFORMATION_EXTRACTION
EMAIL_PROCESSING
AGENT
MULTI_AGENT
MULTIMODAL
GENERAL_LLM
OTHER
```

Para a relação com NER/Information Extraction, classifique:

```text
DIRECT
RELATED
TRANSFERABLE
NONE
```

Definições:

### DIRECT

O artigo estuda explicitamente NER, entity extraction ou information extraction.

### RELATED

O artigo estuda tarefas diretamente próximas, como:

* document information extraction;
* RAG;
* processamento de documentos;
* extração de conteúdo web;
* análise de e-mail;
* pipelines que transformam conteúdo externo em informação estruturada.

### TRANSFERABLE

O trabalho é geral, mas seus ataques ou defesas podem ser aplicados a sistemas de NER ou information extraction.

### NONE

Não há relação identificável.

Justifique a classificação com base no artigo.

---

# 13. Modelos

Extraia todos os modelos utilizados experimentalmente.

Para cada modelo registre:

* nome;
* versão;
* organização, se informada;
* open-source ou proprietary, se declarado;
* papel no experimento;
* attack target;
* evaluator;
* judge;
* guard model;
* generator;
* retriever, quando aplicável.

Não complete versões ausentes.

---

# 14. Datasets

Para cada dataset registre:

* nome;
* origem;
* tamanho;
* tarefa;
* finalidade;
* se é público;
* se foi criado pelos autores;
* quantidade de exemplos utilizados;
* divisão train/test/validation quando informada.

Se o estudo criar um novo dataset, registre isso explicitamente.

---

# 15. Métricas

Extraia todas as métricas utilizadas.

Exemplos possíveis incluem:

```text
ASR
Attack Success Rate
Defense Success Rate
Defense Pass Rate
Accuracy
Precision
Recall
F1
ROC-AUC
False Positive Rate
False Negative Rate
Utility
Helpfulness
Harmlessness
Latency
Cost
```

Não limite a extração a essa lista.

Para cada métrica registre:

* nome;
* definição fornecida pelo artigo;
* finalidade;
* resultado principal;
* unidade;
* tabela/página correspondente.

---

# 16. Protocolo experimental

Extraia detalhadamente:

* threat model;
* número de modelos;
* número de ataques;
* número de prompts;
* número de documentos;
* número de exemplos;
* número de repetições;
* seeds, se informados;
* temperatura;
* parâmetros de geração;
* configuração de retrieval;
* top-k;
* configuração de agentes;
* posição do payload;
* variações do ataque;
* baseline;
* comparação entre métodos;
* configuração de avaliação;
* human evaluation;
* LLM-as-a-judge;
* statistical tests.

Não invente configurações ausentes.

---

# 17. Resultados principais

Extraia resultados quantitativos relevantes.

Cada resultado deve registrar:

* descrição;
* valor;
* métrica;
* modelo;
* ataque;
* defesa, quando houver;
* condição experimental;
* página;
* tabela ou figura.

Priorize resultados diretamente ligados às RQs.

Não tente copiar todas as tabelas do artigo.

---

# 18. Limitações

Separe limitações em três grupos.

## A. Limitações explicitamente declaradas pelos autores

```text
authors_stated_limitations
```

## B. Trabalhos futuros explicitamente sugeridos

```text
authors_stated_future_work
```

## C. Lacunas identificáveis a partir do estudo

```text
review_inferred_gaps
```

Para `review_inferred_gaps`, seja extremamente conservador.

Não apresente uma inferência como se tivesse sido declarada pelos autores.

---

# 19. Evidência negativa

A ausência de informação também é relevante.

Se o artigo:

* não estudar NER;
* não utilizar datasets;
* não propor defesa;
* não avaliar ataques;
* não apresentar threat model;
* não apresentar métricas específicas;

registre explicitamente.

Exemplo:

```json
"ner_directly_investigated": false
```

Não omita silenciosamente.

---

# 20. Relevância para a revisão

Ao final, registre:

```text
VERY_HIGH
HIGH
MODERATE
LOW
OUT_OF_SCOPE
```

Essa classificação deve refletir o **conteúdo do texto completo**, não o score anterior de título/resumo.

Justifique em 2–4 frases.

Não use quantidade desejada de artigos como critério.

---

# 21. Elegibilidade após texto completo

Classifique:

```text
INCLUDE
EXCLUDE
UNCERTAIN
```

Use `EXCLUDE` apenas quando o texto completo demonstrar claramente que o artigo não fornece evidência útil para as perguntas da revisão.

Quando `EXCLUDE`, informe:

```text
full_text_exclusion_reason
```

Exemplos:

```text
NOT_PROMPT_INJECTION
NOT_LLM
NO_RELEVANT_SECURITY_EVIDENCE
PROMPT_INJECTION_TERM_USED_NON_ADVERSARIALLY
DUPLICATE_PUBLICATION
OUT_OF_SCOPE
OTHER
```

---

# 22. Controle de alucinação

Antes de gerar a resposta final, verifique:

1. Todos os dados aparecem no PDF?
2. Modelos foram realmente utilizados ou apenas citados?
3. Datasets foram realmente utilizados ou apenas mencionados?
4. Ataques foram testados ou apenas discutidos?
5. Defesas foram propostas pelos autores ou apenas descritas em related work?
6. Métricas pertencem aos experimentos deste artigo?
7. Resultados quantitativos estão associados à condição correta?
8. Limitações foram declaradas pelos autores ou inferidas?
9. Existe evidência de NER ou information extraction?
10. As páginas e seções realmente correspondem às informações?

Se houver dúvida:

```text
NOT_REPORTED
```

ou:

```text
UNCERTAIN
```

é preferível a inventar informação.

---

# 23. Formato obrigatório de saída

Retorne **exclusivamente um objeto JSON válido**.

Não coloque:

* explicações antes do JSON;
* Markdown;
* ```json;
  ```
* comentários depois do JSON.

Utilize exatamente a seguinte estrutura:

{
"article": {
"title": "",
"authors": [],
"year": "",
"venue": "",
"doi": "",
"publication_type": ""
},

"full_text_assessment": {
"eligibility": "INCLUDE",
"relevance": "VERY_HIGH",
"justification": "",
"full_text_exclusion_reason": null
},

"study_characterization": {
"primary_study_type": "",
"contribution_types": [],
"research_objective": "",
"security_problem": ""
},

"rq1_evidence": {
"summary": "",
"evidence_items": [
{
"finding": "",
"evidence_type": "EXPLICIT",
"page": "",
"section": ""
}
]
},

"rq2_attacks": [
{
"attack_name": "",
"authors_terminology": "",
"attack_category": "",
"direct_or_indirect": "",
"description": "",
"target_component": "",
"attacker_capabilities": [],
"prerequisites": [],
"page": "",
"section": ""
}
],

"rq3_exploitation": [
{
"attack_name": "",
"mechanism": "",
"input_vectors": [],
"entry_point": "",
"payload_description": "",
"attack_objectives": [],
"impact": "",
"page": "",
"section": ""
}
],

"rq4_defenses": [
{
"defense_name": "",
"defense_categories": [],
"description": "",
"pipeline_stage": "",
"target_attacks": [],
"requires_model_modification": null,
"requires_additional_training": null,
"effectiveness": "",
"remaining_vulnerabilities": "",
"limitations": "",
"page": "",
"section": ""
}
],

"rq5_context": {
"tasks": [],
"application_contexts": [],
"ner_directly_investigated": false,
"information_extraction_directly_investigated": false,
"relation_to_ner_information_extraction": "NONE",
"relation_justification": "",
"pages": []
},

"rq6_evaluation": {
"models": [
{
"name": "",
"version": "",
"role": "",
"notes": ""
}
],

```
"datasets": [
  {
    "name": "",
    "origin": "",
    "size": "",
    "purpose": "",
    "created_by_authors": null
  }
],

"metrics": [
  {
    "name": "",
    "definition": "",
    "purpose": ""
  }
],

"baselines": [],

"experimental_protocol": {
  "threat_model": "",
  "number_of_models": "",
  "number_of_examples": "",
  "number_of_prompts": "",
  "number_of_documents": "",
  "number_of_repetitions": "",
  "attack_positions": [],
  "attack_variations": [],
  "generation_parameters": "",
  "retrieval_configuration": "",
  "evaluation_method": "",
  "human_evaluation": "",
  "llm_as_judge": "",
  "statistical_analysis": ""
}
```

},

"key_results": [
{
"description": "",
"value": "",
"metric": "",
"model": "",
"attack": "",
"defense": "",
"experimental_condition": "",
"page": "",
"table_or_figure": ""
}
],

"rq7_limitations_gaps": {
"authors_stated_limitations": [
{
"limitation": "",
"page": "",
"section": ""
}
],

```
"authors_stated_future_work": [
  {
    "future_work": "",
    "page": "",
    "section": ""
  }
],

"review_inferred_gaps": [
  {
    "gap": "",
    "basis": "",
    "page": "",
    "evidence_type": "INFERRED"
  }
]
```

},

"article_contribution_summary": {
"main_contribution": "",
"attack_contribution": "",
"defense_contribution": "",
"evaluation_contribution": "",
"relevance_to_review": ""
},

"evidence_quality_notes": {
"experimental_evidence_present": false,
"attack_empirically_evaluated": false,
"defense_empirically_evaluated": false,
"multiple_models_evaluated": false,
"multiple_datasets_evaluated": false,
"real_world_or_realistic_context": false,
"reproducibility_artifacts_reported": false,
"notes": ""
},

"missing_information": []
}

---

# 24. Regras para arrays vazios

Quando uma categoria não estiver presente no artigo, utilize:

```json
[]
```

Exemplo:

```json
"rq4_defenses": []
```

se o artigo não apresentar defesa.

Não crie objetos vazios apenas para preencher a estrutura.

---

# 25. Regra para NOT_REPORTED

Campos textuais cuja informação deveria existir, mas não foi encontrada, devem utilizar:

```text
NOT_REPORTED
```

Campos booleanos desconhecidos devem utilizar:

```json
null
```

---

# 26. Precisão sobre Related Work

Não confunda trabalhos citados com contribuições do artigo analisado.

Por exemplo:

se o artigo disser:

> Smith et al. proposed a filtering defense.

isso não significa que o artigo atual propôs essa defesa.

Somente coloque uma técnica em `rq4_defenses` como contribuição própria quando ela for utilizada, proposta ou avaliada no estudo atual.

O mesmo vale para:

* ataques;
* modelos;
* datasets;
* métricas;
* resultados.

---

# 27. Identificação de estudos secundários

Se o artigo for:

```text
REVIEW
SURVEY
TAXONOMY
```

adapte a extração.

Nesse caso:

* os ataques podem representar categorias sintetizadas da literatura;
* as defesas podem representar famílias de soluções;
* models/datasets/metrics podem ser relatados como panorama;
* não apresente números agregados como resultados experimentais próprios do artigo;
* registre claramente que a informação provém de síntese secundária.

---

# 28. Resultado esperado

O resultado deve permitir posteriormente:

* comparar artigos;
* agrupar tipos de ataques;
* criar taxonomia de vetores;
* criar taxonomia de objetivos;
* comparar defesas;
* identificar contextos de aplicação;
* identificar modelos e datasets mais utilizados;
* comparar métricas;
* mapear protocolos experimentais;
* analisar relação com NER e information extraction;
* identificar lacunas;
* gerar tabelas da revisão;
* produzir síntese narrativa para o artigo científico.

---

# 29. Execução final

Antes de responder:

1. leia o PDF integralmente;
2. identifique as contribuições próprias do artigo;
3. separe related work das contribuições próprias;
4. extraia ataques;
5. extraia mecanismos e vetores;
6. extraia objetivos;
7. extraia defesas;
8. identifique tarefas e contextos;
9. extraia modelos;
10. extraia datasets;
11. extraia métricas;
12. extraia protocolo experimental;
13. extraia resultados principais;
14. extraia limitações;
15. identifique lacunas;
16. avalie relação com NER/information extraction;
17. determine elegibilidade após texto completo;
18. revise páginas e evidências;
19. valide que não adicionou conhecimento externo;
20. retorne somente o JSON válido.
