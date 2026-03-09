# Contribuindo

Obrigado por contribuir com o `glassdoorcrawler`.

## Fluxo de trabalho

1. Crie uma branch a partir de `master`.
2. Faca mudancas pequenas e focadas em uma issue.
3. Abra um Pull Request para `master`.
4. Resolva todas as conversas de review antes do merge.

Observacao: o repositorio usa regra de protecao na branch padrao, entao mudancas devem entrar via PR.

## Desenvolvimento local

### Setup com pip

```bash
pip install -r requirements.txt
python -m pip install pytest
```

### Setup com poetry

```bash
poetry install
```

## Como validar

```bash
python -m pytest -q
python main.py --pages 1 --no-proxy --output dataset/local/tmp_validacao_1_pagina.xlsx
```

## Outputs locais

- Nao versione arquivos `.xlsx` gerados em execucoes locais.
- Use `dataset/local/` para saidas temporarias de validacao manual.
- Versione apenas datasets curados que precisem ficar em `dataset/`.

## Padroes para issues e PRs

- Vincule a issue correspondente no PR (`Relaciona`/`Fecha`).
- Use labels de release (`release:none`, `release:patch`, `release:minor`, `release:major`) conforme impacto.
- Atualize documentacao quando houver mudanca de comportamento, fluxo ou processo.

## Escopo e qualidade

- Evite misturar refatoracao ampla com correcao funcional no mesmo PR.
- Adicione ou ajuste testes quando alterar parsing, paginacao ou regras de coleta.
- Mantenha o `CHANGELOG.md` coerente com mudancas relevantes de release.
