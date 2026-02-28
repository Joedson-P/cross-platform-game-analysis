# Comparação de Preços Entre Plataformas de Jogos (Steam vs GOG vs Epic)

Este projeto realiza o **Web Scraping**, **Tratamento de Dados** e **Análise Comparativa de Preços** entre três plataformas de jogos digitais para PC. O objetivo é identificar disparidades de preços regionais e encontrar as melhores ofertas para o consumidor brasileiro.

---

## Destaques do Projeto
* **Extração Multiformato**: Coleta de dados via API (Steam), JSON estático (Epic) e Scraper (GOG).

* **Limpeza de Dados (ETL)**: Normalização de nomes de jogos usando Regex para garantir "matches" precisos entre catálogos diferentes.

* **Desafio de Câmbio Regional**: Resolução manual da precificação dinâmica da Valve (USD/BRL) para garantir uma comparação justa no mercado brasileiro.

* **Visualização de _Insights_**: Geração automática de gráficos de economia e dominância de mercado.

---

## Principais Descobertas (Fev/2026)
Com base na última extração, observamos perfis de plataformas distintos:
* **Steam**: Maior variedade de preços e, após normalização, líder em economia para títulos Indie e AA.

* **GOG**: Foco em jogos clássicos e DRM-Free, apresentando as maiores porcentagens de desconto (até 80%).

* **Epic Games**: Foco em títulos AAA de alto orçamento com preços mais tabelados e menos volatilidade.

---

## Tecnologias Utilizadas
* **Python 3.12**

* **Pandas**: Manipulação e unificação de DataFrames.

* **Matplotlib & Seaborn**: Visualização de dados.

* **Requests**: Coleta de dados de APIs.

* **Git**: Controle de versionamento.

---

## Estrutura de Arquivos
* `extract_data_*.py`: Scripts individuais de coleta por loja.

* `unify_and_analyze.py`: Une os datasets e resolve os nomes dos jogos.

* `analyze_best_deals.py`: Algoritmo que identifica a melhor loja para cada título e calcula a economia potencial.

* `visualize_results.py`: Gera os gráficos para o relatório final.

* `reports/`: Contém os CSVs unificados e os gráficos `.png`.

---

## Como Executar
1. Clone o repositório: `git clone ...`

2. Instale as dependências: `pip install -r requirements.txt`

3. Execute o fluxo de análise:
```bash
python unify_and_analyze.py
python analyze_best_deals.py
python visualize_results.py
``` 

---

### Desenvolvido como projeto de análise de dados para o mercado de games.