# SWAPI Characters Pipeline

Ingere todos os personagens da [Star Wars API (SWAPI)](https://swapi.dev/api/people) na tabela `star_wars_api_wender.landing.characters` no Databricks.

## Como funciona

O script roda **localmente** na sua máquina, busca os dados da API com paginação e escreve na tabela Delta via **Databricks Connect**. Isso contorna a limitação de rede do serverless compute do Databricks, que não tem acesso à internet.

```
Sua máquina → requests → swapi.dev (internet)
Sua máquina → Databricks Connect → star_wars_api_wender.landing.characters
```

## Pré-requisitos

- Python 3.10+
- `databricks-connect` instalado
- Perfil `3596016397358328` configurado no `~/.databrickscfg`

### Instalar dependências

```bash
pip install databricks-connect==15.4.*
```

### Verificar configuração do perfil

```bash
databricks auth profiles
```

O perfil `3596016397358328` deve aparecer com status `YES`.

## Como rodar

Na raiz do projeto (`Databricks_Wender`):

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

## Arquivos

| Arquivo | Descrição |
|---|---|
| `swapi_local.py` | Script principal — roda localmente via Databricks Connect |
| `swapi_job.py` | Versão para rodar dentro do Databricks (requer egress de internet liberado) |
| `swapi_characters.py` | Lakeflow Declarative Pipeline (requer egress de internet liberado) |

## Configurações

No topo do `swapi_local.py`:

| Variável | Valor padrão | Descrição |
|---|---|---|
| `TARGET_TABLE` | `star_wars_api_wender.landing.characters` | Tabela de destino |
| `SWAPI_URL` | `https://swapi.dev/api/people/` | Endpoint da API |
| `MAX_RECORDS` | `10000` | Limite de registros por execução |

## Verificar dados carregados

```sql
SELECT * FROM star_wars_api_wender.landing.characters ORDER BY name;
```

```sql
SELECT COUNT(*) FROM star_wars_api_wender.landing.characters;
```

## Observações

- Cada execução faz **overwrite** completo da tabela com o snapshot mais recente da API.
- A SWAPI atualmente tem **82 personagens**, então o limite de 10.000 nunca é atingido.
- Para usar o `swapi_job.py` ou o pipeline Lakeflow diretamente no Databricks, é necessário que o workspace libere egress de internet para o serverless compute (configuração de admin no Account Console).
