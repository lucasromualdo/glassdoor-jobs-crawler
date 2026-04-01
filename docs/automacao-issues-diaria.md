# Automação diária de issues (07:00)

Este repositório agora possui uma rotina automática para governar execução de issues com as regras:

1. Roda diariamente às 07:00 (America/Sao_Paulo) para levantamento das issues.
2. Executa no máximo 1 issue por dia.
3. Para cada execução, cria branch, commit e PR para `master`.
4. Se houver PR pendente de aprovação/merge, não executa nova issue e gera alerta.
5. Se não houver issues abertas, gera alerta.
6. Depois do merge, verifica fechamento da issue e remove branch remanescente.

## Workflows

- `.github/workflows/daily-issue-automation.yml`
  - Seleciona 1 issue aberta por dia (ordem de criação).
  - Bloqueia nova execução se houver PR aberto para `master`.
  - Cria PR automático com referência `Closes #<issue>`.
- `.github/workflows/post-merge-cleanup.yml`
  - Ao merge para `master`, garante fechamento da issue (fallback).
  - Remove a branch relacionada ao PR caso ainda exista.

## Alertas

Os alertas são publicados como issues com títulos:

- `[Alerta Diário] PR pendente de aprovação/merge`
- `[Alerta Diário] Sem issues abertas`

Sugestão: criar uma automação de notificação (e-mail/Slack) filtrando a label `automation-alert`.

## Observação importante

O script `scripts/issue_worker.py` gera um artefato simples para representar a execução diária da issue.
Para implementar resolução real (código/testes), substitua esse script por uma rotina que aplique mudanças do seu domínio.
