# 🚀 VISÃO GERAL


O AutoSAGE automatiza o fluxo completo de decisão orientada a dados:

conecta → ingere → diagnostica → audita → explora → modela → explica → recomenda → expõe em API

Ele foi criado para organizações que precisam clareza, rastreabilidade e confiança, com ou sem um time especializado em ciência de dados.

No AutoSAGE:

nenhuma decisão existe sem diagnóstico,
nenhum modelo existe sem explicação,
e nenhum pipeline existe sem métricas.

[👉 Abrir Relatório Técnico do AutoSAGE](https://sergiofsu1bank.github.io/AutoSAGE/ml_pipeline_report.html)

# 💰 Pitch de Investidor

O AutoSAGE existe porque até 80% do tempo em projetos de dados é gasto limpando, diagnosticando, auditando e explicando dados — não treinando modelos.

As plataformas tradicionais falham em entregar, ao mesmo tempo:

transparência

explicabilidade

auditoria

autonomia ponta a ponta

Com a arquitetura modular DCP → EDA → ML → ORC → Metrics, o AutoSAGE evoluiu de AutoML para uma plataforma de automação científica orientada à decisão e governança.

# ✨ Principais Recursos
## 🔌 Conectividade & Ingestão

Conector nativo para Postgres

Leitura direta de qualquer tabela (schema.table)

Autodetecção de schema e tipos

Carregamento seguro via secrets

Suporte planejado a CSV, DataFrame e SQL

Arquitetura DCP com ingestão totalmente automatizada (v2025)

## 📥 Ingestão Inteligente

Padronização de colunas

Conversão robusta de datas e encodings

Validação inicial de schema

Pipeline orquestrado DCP → EDA

Eliminação de uploads manuais por decisão estratégica

## 🩺 Diagnóstico & Qualidade do Dado

Missing values

Outliers (Z-score, IQR, estatísticas robustas)

Cardinalidade e estrutura

Drift estrutural

Estatísticas descritivas e distribuições

## 🔬 Auto-EDA

Correlações (Pearson, Spearman, Cramér’s V)

Testes de hipótese (t-test, ANOVA, χ²)

Insights pré-modelagem

Identificação de variáveis fracas

Visualizações automáticas

Exportação oficial de artefatos em PARQUET

## 🤖 Seleção Automática de Modelos

Classificação: Logistic, SVM, Random Forest, Gradient Boosting

Regressão: Linear, Ridge, Random Forest, XGBoost

Escolha baseada em:

estabilidade

interpretabilidade

viés–variância

Módulo ML isolado, versionado e reprodutível

## 🏋️ Treinamento

Train/test split estratificado

Normalização e encoding automáticos

Cross-validation

Busca simples de hiperparâmetros

Pipelines reprodutíveis

Execução totalmente autônoma dentro do container ML

## 📊 Métricas & Comparações

Classificação → AUC, F1, Precision, Recall

Regressão → RMSE, MAE, R², MAPE

Comparação obrigatória com baseline

Relatórios HTML gerados automaticamente

## 📈 Monitoramento & Logs

O módulo de Metrics é a camada central de governança, rastreabilidade e confiança do AutoSAGE.

Nada no pipeline existe se não for medido, registrado e auditável.

O que o módulo monitora

Execuções completas do pipeline

Estado real de cada etapa

Falhas, tempos e gargalos

Relação entre dado, modelo e decisão

Métricas registradas (por contrato)

trace_id

pipeline (DCP, EDA, ML, ORC)

stage

status (STARTED | COMPLETED | FAILED)

duration_ms

dataset_name

vendor

pipeline_version

error_code / error_message

Essas informações são persistidas em tabelas próprias de monitoramento.

Metrics como controle de fluxo

Execuções duplicadas são rejeitadas por trace_id

Falhas interrompem automaticamente etapas downstream

Nenhuma execução avança sem estado consistente

Não existem falhas silenciosas

Se não foi medido, não aconteceu.

## 🔎 Explicabilidade

Importância de features

SHAP values

Análise de comportamento do modelo

Identificação de vieses e riscos

## 📦 Exportação & Registry

Salvamento automático do melhor modelo (/models/)

Artefatos exportados:

Modelo

Métricas

Feature importance

Logs

Arquivos PARQUET

Versionamento por hash de execução

Registry único compartilhado entre módulos via Docker volumes

## 📡 API de Inferência

FastAPI em src/app/main.py

Endpoint /predict

Validação automática via Pydantic

Carregamento dinâmico via registry

Retorno com previsão + explicabilidade

Logging estruturado por requisição

📈 Logs & Auditoria

Logs persistidos em /logs/

IDs de execução

Warnings de drift

Auditoria completa do pipeline

Trace ID distribuído entre ORC → DCP → EDA → ML

## 🆕 Arquitetura Modular 2025

ORC: orquestra e valida o fluxo

DCP: coleta e padroniza dados

EDA: diagnostica, audita e prepara artefatos

ML: treina, avalia e explica

Metrics: monitora, governa e prova

Tudo conectado por registry versionado + trace ID distribuído.

# 🔬 Metodologia Científica

## 1️⃣ Ingestão & Padronização
- Tipagem automática
- Normalização de colunas
- Conversão e validação de datas
- **Pipeline padronizado no módulo DCP**

## 2️⃣ Diagnóstico Estatístico
- Distribuições e densidades
- Estatísticas descritivas
- Cardinalidade
- **Artefatos agora exportados em PARQUET**

## 3️⃣ Auditoria de Qualidade
- Missing values
- Outliers
- Inconsistências semânticas
- Drift estrutural

## 4️⃣ Relações & Sinal Estatístico
- Correlações
- Testes de hipótese
- Feature importance preliminar

## 5️⃣ Seleção Inteligente de Modelos
- Baseado no target e estrutura de variáveis

## 6️⃣ Treinamento Reprodutível
- Splits estratificados
- Encodings e escalas automáticas
- Cross-validation
- **Execução isolada no módulo ML**

## 7️⃣ Métricas Transparentes
- Classificação e regressão completas

## 8️⃣ Explicabilidade
- SHAP
- Importância
- Detecção de vieses

## 9️⃣ Recomendação Acionável
- Caminhos sugeridos
- Próximos passos
- Riscos e limitações

## ⚔️ Comparação Estratégica

| Plataforma | Pontos Fortes | Limitações | O que o AutoSAGE faz melhor |
|------------|---------------|------------|------------------------------|
| Google AutoML | Treina rápido | Caixa-preta | Transparência + diagnóstico |
| AWS Autopilot | Escala | Complexidade | Simples, direto e acessível |
| Azure AutoML | Interface | Dependência Azure | Controle total |
| DataRobot | Governança | Muito caro | Open-source e leve |
| H2O DAI | Automação | Complexo para negócios | Foco em decisão |
| PyCaret | Simples | Assume dado limpo | Auditoria + limpeza |
| AutoGluon/Sklearn | Performance | Caixa-preta | Relatórios explicáveis |
| **AutoSAGE** | Decisão orientada a dados | Em evolução | Clareza + ação imediata |

# 🎯 Mercado-Alvo

PMEs

Consultorias

Startups (fintech, healthtech, edtech)

Times de produto e growth

Empresas sem time de dados

# 💵 Monetização

Versão enterprise

Suporte premium

Plugins (MLOps, dashboards, APIs)

Hosted SaaS

# 🧠 Vantagens Estratégicas

Open-source, auditável e transparente

Arquitetura modular e escalável

Métricas como núcleo do sistema

Decisão antes de previsão

Pipelines científicos governáveis

Pronto para ambientes enterprise

# 🌎 Visão

Se existe dado, deveria existir clareza.
E clareza deveria ser automática.

O AutoSAGE é a camada entre dados, decisões e confiança operacional.


# 📊 Documentação

- Arquitetura → `docs/architecture.md`
- Relatório técnico → `docs/ml_pipeline_report.html`
- Roadmap → `ROADMAP.md`
- Contribuição → `CONTRIBUTING.md`

---

# 🛡️ Licença
MIT

---

# 💡 Contato
🔗 https://www.linkedin.com/in/sergiofonsecasilva  
📩 sergiofs.u1tec@gmail.com  
📞 +55 11 9 3767-8996
