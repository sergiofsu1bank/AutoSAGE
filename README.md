# AutoSAGE

Plataforma de IA que transforma dados brutos em diagnóstico, modelagem, explicabilidade e recomendações acionáveis — totalmente automatizada, integrada e pronta para produção.

[👉 Abrir Relatório Técnico do AutoSAGE](https://sergiofsu1bank.github.io/AutoSAGE/ml_pipeline_report.html)

---

# 🚀 Visão Geral

O AutoSAGE automatiza o fluxo completo:

**conecta → ingere → diagnostica → audita → explora → modela → explica → recomenda → expõe em API**

Criado para empresas que precisam clareza, velocidade e decisões orientadas a dados — com ou sem um time especializado.

---

# 💰 Pitch de Investidor

O AutoSAGE existe porque **80% do tempo em ciência de dados é perdido limpando, diagnosticando e explicando dados** — não modelando.

Nenhuma plataforma líder resolve esse gap com:

- transparência  
- explicabilidade  
- auditoria  
- autonomia de ponta a ponta  

Com a nova arquitetura modular (DCP → EDA → ML → ORC), o AutoSAGE evoluiu para uma **plataforma de automação científica**, não apenas AutoML.

---

# ✨ Principais Recursos

## 🔌 Conectividade & Ingestão
- Conector nativo para **Postgres**
- Leitura direta de qualquer tabela (`schema.table`)
- Autodetecção de schema e tipos
- Carregamento seguro via secrets
- Suporte a DataFrame, CSV e SQL (roadmap)
- **Novo (v2025): arquitetura DCP com ingestão totalmente automatizada**

## 📥 Ingestão Inteligente
- Padronização de colunas
- Detecção automática do target
- Conversão robusta de datas e encodings
- Validação inicial do schema
- **Pipeline orquestrado via módulo DCP → EDA**

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
- **Exportação agora 100% em PARQUET (novo padrão oficial)**

## 🤖 Seleção Automática de Modelos
- Classificação: Logistic, SVM, Random Forest, Gradient Boosting
- Regressão: Linear, Ridge, Random Forest, XGBoost
- Escolha baseada em bias–variance, estabilidade e interpretabilidade
- **Integração com novo módulo ML 100% isolado e versionado**

## 🏋️ Treinamento
- Train/test split estratificado
- Normalização e encoding automáticos
- Cross-validation
- Busca simples de hiperparâmetros
- Pipeline reprodutível
- **Arquitetura atual executa todo treinamento dentro do container ML de forma autônoma**

## 📊 Métricas & Comparações
- Classificação → AUC, F1, Precision, Recall
- Regressão → RMSE, MAE, R², MAPE
- Comparação com baseline obrigatório
- **Relatórios HTML completos gerados automaticamente**

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
  - **Arquivos PARQUET**
- Versionamento interno via hash de execução
- **Registry único compartilhado entre módulos via Docker volumes**

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
- **Trace ID propagado entre todos os módulos (ORC → DCP → EDA → ML)**

## 🆕 🔧 Módulo de Conectores DCP
O módulo DCP (Data Connector Pipeline) é a nova camada do AutoSAGE para conectar bancos de dados externos e ingerir tabelas automaticamente, sem depender de uploads manuais.

### O que foi implementado
- Conector Postgres totalmente operacional  
- Ingestão direta da tabela `customer_churn` do banco `dcp`  
- Carregamento seguro de credenciais via Secrets Manager  
- Registry interno para configurações  
- Logs estruturados e padronizados  
- Endpoint `/ingest` para disparo da coleta  
- Pipeline automático **DCP → EDA → ML**  
- Eliminado o upload manual por decisão estratégica  

### Pronto para expansão
- MySQL  
- SQL Server  
- BigQuery  
- S3  
- APIs REST externas  

### Filosofia
- Conectores plugáveis  
- Execução orquestrada e segura  
- Arquitetura preparada para ambientes enterprise  

### 🆕 Arquitetura Modulada 2025
- **ORC (Orchestrator):** controla e garante o fluxo completo  
- **DCP:** coleta e padroniza  
- **EDA:** diagnostica, audita e prepara os artefatos  
- **ML:** modela, avalia e gera relatórios  
- Todos conectados por **registry versionado + trace ID distribuído**  

---

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

- Open-source, transparente e auditável
- Arquitetura modular (DCP → EDA → ML → ORC), leve e escalável
- Explicabilidade total: cada decisão do pipeline é registrada, rastreável e justificável
- Foco absoluto em decisão, não apenas previsão
- Pipelines científicos reprodutíveis, versionados e governáveis
- Compatível com ambientes enterprise (containers isolados, registry compartilhado, trace-id distribuído)
---

# 🌎 Visão

Se existe dado, deveria existir clareza.  
E clareza deveria ser automática.

Estamos construindo a camada universal de interpretação entre o dado e a decisão — agora com uma **arquitetura distribuída, escalável e pronta para produção real**.

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
