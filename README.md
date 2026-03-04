<div align="center">

<img src="https://avatars.githubusercontent.com/u/76263028" width="80" alt="Anthropic Claude" />

# Databricks SWAPI Pipeline

**Pipeline de ingestão de personagens Star Wars no Databricks**
*Construído com Databricks Connect + Claude Code*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Databricks](https://img.shields.io/badge/Databricks-Connect-FF3621?style=for-the-badge&logo=databricks&logoColor=white)](https://databricks.com)
[![Claude](https://img.shields.io/badge/Built%20with-Claude%20Code-black?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## Sobre o Projeto

Este projeto ingere todos os personagens da [Star Wars API (SWAPI)](https://swapi.dev) na tabela Delta `star_wars_api_wender.landing.characters` no Databricks Unity Catalog, utilizando **Databricks Connect** para superar limitações de rede do serverless compute.

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Máquina Local                        │
│                                                         │
│  swapi_local.py                                         │
│       │                                                 │
│       ├── requests.get() ──► swapi.dev/api/people/      │
│       │        (internet local)                         │
│       │                                                 │
│       └── spark.write() ──► Databricks Connect          │
│                                    │                    │
└────────────────────────────────────┼────────────────────┘
                                     │
                          ┌──────────▼──────────┐
                          │     Databricks GCP  │
                          │                     │
                          │  star_wars_api_wender│
                          │    └── landing       │
                          │         └── characters│
                          └─────────────────────┘
```

## Estrutura do Projeto

```
📦 databricks-swapi-pipeline
 ┣ 📂 pipelines
 ┃  └── 📂 swapi_characters
 ┃       ┣ 📄 swapi_local.py        ← Script principal (Databricks Connect)
 ┃       ┣ 📄 swapi_job.py          ← Versão para rodar no Databricks
 ┃       ┣ 📄 swapi_characters.py   ← Lakeflow Declarative Pipeline
 ┃       └── 📄 README.md           ← Instruções detalhadas
 ┣ 📄 .env.example                  ← Template de variáveis de ambiente
 ┣ 📄 .gitignore
 └── 📄 README.md
```

## Primeiros Passos (do zero ao funcionando)

### 1. Pré-requisitos

- Python **3.10+**
- [Databricks CLI](https://docs.databricks.com/en/dev-tools/cli/install.html) instalado
- Acesso a um workspace Databricks com Unity Catalog

### 2. Clone e instale as dependências

```bash
git clone https://github.com/wendermezin/databricks-swapi-pipeline.git
cd databricks-swapi-pipeline

pip install databricks-connect==15.4.* python-dotenv requests
```

### 3. Autentique no Databricks

```bash
databricks configure
```

Informe a URL do seu workspace e o token de acesso. Para ver os perfis configurados:

```bash
databricks auth profiles
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com o nome do seu perfil:

```env
DATABRICKS_CONFIG_PROFILE=nome_do_seu_profile
```

### 5. Crie os objetos no Databricks

Execute os comandos abaixo no Databricks SQL Editor ou via CLI:

```sql
CREATE CATALOG IF NOT EXISTS star_wars_api_wender;

CREATE SCHEMA IF NOT EXISTS star_wars_api_wender.landing;

CREATE TABLE IF NOT EXISTS star_wars_api_wender.landing.characters (
  name       STRING,
  height     STRING,
  mass       STRING,
  birth_year STRING,
  homeworld  STRING
);
```

### 6. Execute o pipeline

```bash
python pipelines/swapi_characters/swapi_local.py
```

### 7. Verifique os dados

```sql
SELECT * FROM star_wars_api_wender.landing.characters ORDER BY name;
SELECT COUNT(*) AS total FROM star_wars_api_wender.landing.characters;
```

## Como Rodar (execuções seguintes)

```bash
python pipelines/swapi_characters/swapi_local.py
```

### Saída esperada

```
Fetching Star Wars characters from SWAPI (running locally)...
Fetched 10 characters so far (limit: 10000)...
Fetched 20 characters so far (limit: 10000)...
...
Fetched 82 characters so far (limit: 10000)...
Total characters fetched: 82
Successfully loaded 82 characters into star_wars_api_wender.landing.characters
```

## Tabela de Destino

| Coluna | Tipo | Descrição |
|---|---|---|
| `name` | STRING | Nome do personagem |
| `height` | STRING | Altura em cm |
| `mass` | STRING | Massa em kg |
| `birth_year` | STRING | Ano de nascimento |
| `homeworld` | STRING | URL do planeta natal |

### Verificar dados

```sql
SELECT * FROM star_wars_api_wender.landing.characters ORDER BY name;

SELECT COUNT(*) AS total FROM star_wars_api_wender.landing.characters;
```

## Por que Databricks Connect?

O serverless compute do Databricks não tem acesso à internet por padrão. Com Databricks Connect:

- ✅ `requests` roda **localmente** (tem internet)
- ✅ `spark.write()` envia dados para o **Databricks remoto**
- ✅ Sem necessidade de liberar egress no workspace

## Recursos Criados no Databricks

| Recurso | Nome | Tipo |
|---|---|---|
| Catalog | `star_wars_api_wender` | Unity Catalog |
| Schema | `landing` | Schema |
| Table | `characters` | Delta Table |
| Pipeline | `swapi_characters_landing` | Lakeflow Pipeline |
| Job | `swapi_characters_ingest` | Serverless Job |

---

<div align="center">

**Desenvolvido com** ❤️ **usando [Claude Code](https://claude.ai/claude-code) + [Databricks](https://databricks.com)**

</div>
