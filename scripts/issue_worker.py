from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera artefato mínimo para execução diária de issue."
    )
    parser.add_argument("--issue-number", required=True, type=int)
    parser.add_argument("--issue-title", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    out_dir = Path("docs/daily-issue-runs")
    out_dir.mkdir(parents=True, exist_ok=True)

    file_path = out_dir / f"issue-{args.issue_number}.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    file_path.write_text(
        "\n".join(
            [
                f"# Execução diária da issue #{args.issue_number}",
                "",
                f"- Título: {args.issue_title}",
                f"- Executado em: {timestamp}",
                "- Status: PR aberto para aprovação",
                "",
                "> Substitua este gerador pelo fluxo real de implementação da issue.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
