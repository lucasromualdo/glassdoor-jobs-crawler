# glassdoorcrawler

Crawler para coletar dados de vagas no Glassdoor e exportar para Excel.

## Estrutura do projeto

- `glassdoorcrawler/scraper.py`: logica de coleta e parsing
- `glassdoorcrawler/cli.py`: interface de linha de comando
- `main.py`: ponto de entrada compativel com o script antigo

## Instalacao

### Com `pip`

```bash
pip install -r requirements.txt
```

### Com `poetry`

```bash
poetry install
```

## Uso

```bash
python main.py --pages 1 --output dataset/local/belohorizonte_vagas.xlsx
```

Se seu ambiente tiver proxies configurados (ex.: `HTTP_PROXY`) e voce quiser ignorar isso no teste local:

```bash
python main.py --pages 1 --no-proxy
```

Ou via `poetry`:

```bash
poetry run glassdoorcrawler --pages 1
```

## Limites do crawler

- O HTML do Glassdoor muda com frequencia; ajustes no parsing podem ser necessarios.
- O crawler usa atraso entre requisicoes (`--delay`) para reduzir bloqueios.
- Quando o Glassdoor retorna a pagina de seguranca do Cloudflare, o scraper tenta fallback automatico via `curl_cffi` (requer dependencias instaladas).
- Mesmo com fallback, bloqueios temporarios podem impedir a coleta parcial ou total.

## Politica de outputs locais

- Planilhas geradas pelo CLI (`.xlsx`) sao artefatos locais por padrao.
- Para execucao local, salve outputs em `dataset/local/` (ex.: `dataset/local/belohorizonte_vagas.xlsx`).
- Apenas datasets curados em `dataset/` devem ser versionados no repositorio.

## Fluxo basico de contribuicao

1. Crie uma branch a partir de `master`.
2. Faca mudancas pequenas e focadas em uma issue.
3. Abra um Pull Request para `master`.
4. Resolva as conversas de review antes do merge.

Mais detalhes: `CONTRIBUTING.md`.

## Manutencao

- Regras do repositorio e ordem sugerida de backlog: `docs/manutencao-regras-e-backlog.md`
- Registro de decisao do ruleset da branch `master`: `docs/decisao-ruleset-master.md`
- Processo de release e checklist: `docs/release-process.md`
- Historico de mudancas por versao: `CHANGELOG.md`
- Classificacao de impacto de release (`release:*`) registrada em issues/PRs para apoiar SemVer

## Governanca

- Licenca do projeto: `LICENSE`
- Guia de contribuicao: `CONTRIBUTING.md`
- Politica de seguranca: `SECURITY.md`
- Responsaveis por revisao de caminhos: `.github/CODEOWNERS`
