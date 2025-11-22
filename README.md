<p align="center">
  <img src="docs/hero-banner.png" alt="AutoSAGE Banner" width="100%">
</p>

<h1 align="center">AutoSAGE</h1>

<p align="center">
  Plataforma de IA para diagnóstico de dados, Auto-EDA, seleção automática de modelos, explicabilidade e recomendações acionáveis.
</p>

<p align="center">
  <a href="#">🚧 Em desenvolvimento ativo</a> •
  <a href="LICENSE">MIT License</a> •
  <a href="CONTRIBUTING.md">Contribuir</a>
</p>

---

## 🚀 O que é o AutoSAGE?

O AutoSAGE ingere dados, avalia qualidade, explora, modela, explica e recomenda — tudo automaticamente.

Ideal para:
- Cientistas e Engenheiros de Dados
- Analistas de Negócio
- Times de Produto e Growth
- Empresas sem time de IA

Da bagunça ao insight — em minutos.

---

## ✨ Principais recursos

✅ Ingestão fácil: CSV, SQL, DataFrame  
✅ Diagnóstico automático do dataset  
✅ Auto-EDA com visualizações  
✅ Seleção inteligente do melhor modelo  
✅ Treinamento automatizado  
✅ Explicabilidade integrada  
✅ Recomendações acionáveis  
✅ Relatório exportável  

---

## 🔬 Metodologia Científica do AutoSAGE

O AutoSAGE segue rigor estatístico e boas práticas de ciência de dados para transformar dados brutos em decisões acionáveis.  
Nada de “modelo na sorte” — cada etapa é guiada por fundamentos matemáticos, estatísticos e computacionais.

### 1️⃣ Ingestão & Padronização
- Detecção automática de schema
- Identificação de tipos (numérico, categórico, temporal, texto)
- Normalização de nomes de colunas
- Conversão segura de encoding e datas

### 2️⃣ Diagnóstico Estatístico do Dataset
- Distribuições univariadas e densidade
- Medidas descritivas (média, mediana, variância, assimetria, curtose)
- Tamanho da amostra e cobertura
- Avaliação de cardinalidade de variáveis

### 3️⃣ Auditoria de Qualidade do Dado
- Detecção de valores ausentes
- Outliers via Z-score, IQR e robust statistics
- Inconsistências semânticas e lógicas
- Duplicidade e drift estrutural

### 4️⃣ Relações, Hipóteses & Sinal Estatístico
- Correlações (Pearson, Spearman, Cramér’s V)
- Testes de hipótese (t-test, ANOVA, χ²)
- Importância preliminar de features
- Identificação de variáveis irrelevantes ou redundantes

### 5️⃣ Seleção Inteligente de Modelos
Com base na natureza do target:
- Regressão → Linear, Ridge, Random Forest, XGBoost
- Classificação → Logistic, SVM, Random Forest, Gradient Boosting
- Time series (futuro roadmap)

Escolha guiada por:
- Bias–variance trade-off
- Robustez estatística
- Interpretabilidade

### 6️⃣ Treinamento Reprodutível
- Train/test split estratificado
- Normalização e encoding automáticos
- Busca de hiperparâmetros balanceada
- Cross-validation para generalização

### 7️⃣ Métricas Transparentes
- Classificação → AUC, F1, recall, precision, matriz de confusão
- Regressão → RMSE, MAE, R², MAPE
- Comparação entre modelos e baseline obrigatório

### 8️⃣ Explicabilidade & Interpretabilidade
- Feature importance
- SHAP values
- Insights sobre comportamento do modelo
- Detecção de potenciais vieses

### 9️⃣ Recomendação Acionável
- Caminhos analíticos sugeridos
- Melhor modelo para o cenário
- Riscos, limitações e próximos passos
- Sugestões para coleta, limpeza e engenharia de features

---

✅ Metodologia clara  
✅ Mostra ciência, não “mágica”  
✅ Aumenta confiança de investidores, usuários e contribuidores  
✅ Reforça credibilidade do projeto

## 🧰 Recursos adicionais do AutoSAGE

Além do pipeline inteligente de ingestão, diagnóstico, EDA, modelagem e explicabilidade, o AutoSAGE oferece recursos operacionais para uso real em times de dados:

### ✅ Logging estruturado
- Logs padronizados por etapa da pipeline
- Níveis configuráveis (`INFO`, `DEBUG`, `WARNING`, `ERROR`)
- Persistência opcional em arquivo `.log`
- Rastreamento completo para auditoria e troubleshooting

### ✅ Relatórios automáticos
- Sumário do dataset
- Qualidade do dado e recomendações de limpeza
- Comparação entre modelos
- Interpretação e insights acionáveis
- Exportável em HTML, PDF ou Markdown (roadmap)

### ✅ Versionamento & Reprodutibilidade
- Registro de parâmetros, métricas e modelos
- Hash do dataset para rastreabilidade
- Execuções reprodutíveis

### ✅ Exportação de artefatos
- Modelo treinado (`.pkl`)
- Métricas de avaliação
- Feature importance
- Visualizações do Auto-EDA

### ✅ Configuração flexível
- YAML, JSON ou argumentos diretos em Python
- Ajuste de seed, estratégia de split, métricas, imputação etc.

### ✅ CLI (em desenvolvimento)
Execute tudo sem abrir Python:

## ⚡ Exemplo em 15 segundos

```python
from autosage import AutoSAGE

sage = AutoSAGE()

sage.ingest("banco_churn.csv")
sage.validate()
sage.auto_eda()
sage.train()
sage.explain()
sage.recommend()
```
## 💡 Contato

🔗 LinkedIn — https://www.linkedin.com/in/sergiofonsecasilva  
📩 E-mail — sergiofs@gmail.com
