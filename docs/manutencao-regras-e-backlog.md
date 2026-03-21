# Manutencao: Ruleset e Proximos Passos

Atualizado em: 2026-03-20

## Ruleset atual (branch padrao `master`)

Ruleset ativo: `Protect default branch (PR + conversation resolution)`

Regras aplicadas:

- Bloqueia exclusao da branch (`deletion`)
- Bloqueia force-push (`non_fast_forward`)
- Exige PR para merge (`pull_request`)
- Exige resolucao de conversas de review antes do merge
- Nao exige approvals (por enquanto)
- Nao exige status checks obrigatorios no ruleset (por enquanto)

Observacao:

- Sem bypass configurado (ate o owner precisa seguir PR + resolucao de conversas)

## CI atual (estado vigente)

Workflow ativo: `.github/workflows/ci.yml`

- Executa em `push` e `pull_request` para `master`
- Roda matriz de Python `3.10` e `3.12`
- Faz checks basicos (`compileall` e `pip check`) e testes (`pytest -q`)

## Quando revisar esse ruleset

Rever quando:

- Promover status checks da CI para obrigatorios no ruleset
- Comecar a receber contribuicoes externas
- Precisar acelerar hotfix (avaliar bypass admin)

## Status rapido do backlog (2026-03-20)

- `#29` aberta: alinhar default de output com politica `dataset/local`
- `#30` aberta: robustecer contrato de sessao HTTP na paginacao BFF
- `#31` aberta: atualizar documentacao de manutencao para estado vigente de CI/ruleset

## Convencao atual: backlog x releases

### Milestones (versao/release)

Usar milestones para representar versoes/releases, por exemplo:

- `v0.1.0`
- `v0.1.1`
- `v0.2.0`

Uso recomendado:

- Vincular issues com impacto no release atual (ex.: `release:patch`, `release:minor`)
- Vincular PRs que entregam itens daquele release
- Fechar o milestone quando a versao for publicada

### Labels de backlog (planejamento)

Usar labels para agrupar frentes/ciclos de trabalho no backlog:

- `backlog:ciclo-a`: ciclo funcional do crawler (execucao, parser, paginacao, testes/CI)
- `backlog:ciclo-b`: ciclo de governanca/manutencao (docs, repo, automacoes)

Motivo da separacao:

- Evita usar milestone para dois objetivos diferentes ao mesmo tempo (planejamento e release)
- Facilita visualizar o que entra na proxima versao vs. o que continua no backlog

### Estado atual (aplicado em 2026-03-20)

- Milestone de release ativo: `v0.1.0`
- `#2` mantida no backlog com label `backlog:ciclo-a` (sem milestone de versao)
- `#5`, `#10`, `#11`, `#12` mantidas no backlog com label `backlog:ciclo-b` (sem milestone de versao)

## Proximas issues (ordem sugerida)

Observacao:

- A ordem abaixo continua valendo como prioridade de backlog.
- Atribuir milestone de versao apenas quando a issue entrar de fato no release.

1. `#30` robustecer contrato de sessao HTTP na paginacao BFF
2. `#29` alinhar default de output com politica `dataset/local`
3. `#31` manter documentacao de governanca sincronizada com CI/ruleset
4. `#2` adicionar testes de parsing e paginacao
5. `#3` atualizar dependencias e regenerar `poetry.lock`
6. `#12` adicionar LICENSE e documentos de governanca
7. `#11` configurar Dependabot
8. `#10` remover artefato versionado da raiz e ajustar politica de outputs
9. `#5` melhorar documentacao (README / limitacoes / contribuicao)

## Classificacao de release (SemVer)

As issues agora usam labels `release:*` para indicar impacto de versao:

- `release:none`: docs/infra/processo/testes sem impacto funcional direto
- `release:patch`: correcoes/ajustes compativeis
- `release:minor`: mudancas relevantes compativeis
- `release:major`: mudancas incompativeis/importantes

Referencia detalhada: `docs/release-process.md`

## Separacao pratica para releases (resumo)

- Ciclo A (label `backlog:ciclo-a`): `#1`, `#4`, `#3` + recomendado `#2`
- Ciclo B (label `backlog:ciclo-b`): `#12`, `#11`, `#10`, `#5`
- Concluidas relevantes para historico de release: `#6`, `#8`, `#16`

Exemplo de uso com milestone:

- Release `v0.1.0`: `#1`, `#4`, `#3` (e PR que entrega esses itens)

## Ajustes de ruleset com CI ativo

Com workflow de testes ativo, proximo passo recomendado:

1. Exigir status checks obrigatorios (ex.: testes)
2. Opcional: exigir `1` approval
3. Opcional: manter/ajustar regra de resolucao de conversas

## Dica de manutencao

Sempre que decidir algo de repositorio (ruleset, fluxo de PR, CI), registrar:

- O que foi decidido
- Motivo
- Data
- Quando revisar novamente

## Registros de decisao

- Ruleset da `master`: `docs/decisao-ruleset-master.md`
