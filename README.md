# AutoSAGE

Plataforma de IA que transforma dados brutos em diagnóstico, modelagem, explicabilidade e recomendações acionáveis — totalmente automatizada, integrada e pronta para produção.

---

# 🚀 Visão Geral

O AutoSAGE automatiza o fluxo completo:

**conecta → ingere → diagnostica → audita → explora → modela → explica → recomenda → expõe em API**

Criado para empresas que precisam clareza, velocidade e decisões orientadas a dados — com ou sem um time especializado.

---

# ✨ Principais Recursos

## 🔌 Conectividade & Ingestão
- Conector nativo para **Postgres**
- Leitura direta de qualquer tabela (`schema.table`)
- Autodetecção de schema e tipos
- Carregamento seguro via secrets
- Suporte a DataFrame, CSV e SQL (roadmap)

## 📥 Ingestão Inteligente
- Padronização de colunas
- Detecção automática do target
- Conversão robusta de datas e encodings
- Validação inicial do schema

## 🩺 Diagnóstico & Qualidade do Dado
- Missing values
- Outliers (Z-score, IQR, robust stats)
- Cardinalidade e estrutura
- Drift estrutural
- Estatísticas descritivas e distribuições

## 🔬 Auto-EDA
- Correlações (Pearson, Spearman, Cramér’s V)
- Testes de hipótese (t-test, ANOVA, χ²)
- Insights pré-modelagem
- Identificação de variáveis fracas
- Visualizações automáticas

## 🤖 Seleção Automática de Modelos
- Classificação: Logistic, SVM, Random Forest, Gradient Boosting
- Regressão: Linear, Ridge, Random Forest, XGBoost
- Escolha baseada em bias–variance, estabilidade e interpretabilidade

## 🏋️ Treinamento
- Train/test split estratificado
- Normalização e encoding automáticos
- Cross-validation
- Busca simples de hiperparâmetros
- Pipeline reprodutível

## 📊 Métricas & Comparações
- Classificação → AUC, F1, Precision, Recall
- Regressão → RMSE, MAE, R², MAPE
- Comparação com baseline obrigatório

## 🔎 Explicabilidade
- Importância de features
- SHAP values
- Análise de comportamento do modelo
- Identificação de vieses

## 📦 Exportação & Registry
- Salvamento automático do melhor modelo (`/models/`)
- Artefatos exportados:
  - Modelo
  - Métricas
  - Feature importance
  - Logs
- Versionamento interno via hash de execução

## 📡 API de Inferência (implementada)
- FastAPI em `src/app/main.py`
- Endpoint `/predict`
- Validação automática via Pydantic
- Carregamento do modelo via registry
- Retorno com previsão + explicabilidade
- Logging estruturado por requisição

## 📈 Monitoramento & Logs
- Logs persistidos em `/logs/`
- IDs de execução
- Drift warnings
- Auditoria completa do pipeline

## 🆕 🔧 Módulo de Conectores DCP
O módulo DCP (Data Connector Pipeline) é a nova camada do AutoSAGE para conectar bancos de dados externos e ingerir tabelas automaticamente, sem depender de uploads manuais.
O que foi implementado

Conector Postgres totalmente operacional
Ingestão direta da tabela customer_churn do banco dcp
Carregamento seguro de credenciais via Secrets Manager
Registry interno para configurações
Logs estruturados e padronizados
Endpoint /ingest para disparo da coleta
Alinhamento com a decisão estratégica: eliminar upload manual e focar em conectores nativos
Pronto para expansão
MySQL
SQL Server
BigQuery
S3
APIs REST externas

Filosofia
Conectores plugáveis
Execução orquestrada e segura
Arquitetura preparada para ambientes enterprise
---

# 🔬 Metodologia Científica

## 1️⃣ Ingestão & Padronização
- Tipagem automática
- Normalização de colunas
- Conversão e validação de datas

## 2️⃣ Diagnóstico Estatístico
- Distribuições e densidades
- Estatísticas descritivas
- Cardinalidade

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

---

# ⚔️ Comparação Estratégica

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

---

# 💰 Pitch de Investidor

O AutoSAGE existe porque **80% do tempo em ciência de dados é perdido limpando, diagnosticando e explicando dados**, não modelando.

Nenhuma plataforma líder resolve esse gap de forma simples, transparente e acessível.

O AutoSAGE transforma qualquer dataset em:

- diagnóstico completo
- narrativa explicável
- modelo reproduzível
- previsões auditáveis
- recomendações acionáveis

Enquanto AutoML tradicional responde *“qual modelo usar?”*,
o AutoSAGE responde **“o que está acontecendo e o que fazer agora?”**

---

# 🎯 Mercado-Alvo
- PMEs
- Consultorias
- Startups (fintech, healthtech, edtech)
- Times de produto e growth
- Empresas sem time de dados

# 💵 Monetização
- Versão enterprise
- Suporte premium
- Plugins (MLOps, dashboards, APIs)
- Hosted SaaS

# 🧠 Vantagens Estratégicas
- Open-source
- Simples e leve
- 100% explicável
- Foco em decisão
- Pipeline auditável

---

# 🌎 Visão

Se existe dado, deveria existir clareza.
E clareza deveria ser automática.

Estamos construindo a camada universal de interpretação entre o dado e a decisão.

---

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
🔗 LinkedIn — https://www.linkedin.com/in/sergiofonsecasilva
📩 sergiofs.u1tec@gmail.com
📞 +55 11 9 3767-8996
