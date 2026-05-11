import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.review_pipeline import ReviewPipeline


console = Console()


def main():
    """
    Generate Markdown and JSON review reports.

    Usage:
        python src/generate_report.py data/sample_contracts/sample_contract.txt
    """

    if len(sys.argv) < 2:
        console.print("[red]Please provide a contract file path.[/red]")
        console.print("Example:")
        console.print("python src/generate_report.py data/sample_contracts/sample_contract.txt")
        return

    file_path = sys.argv[1]

    pipeline = ReviewPipeline()
    output = pipeline.run(file_path)

    loaded = output["loaded"]
    classification = output["classification"]
    clauses = output["clauses"]
    payload = output["payload"]
    markdown_report = output["markdown_report"]

    stem = Path(loaded["file_name"]).stem
    md_path = PROJECT_ROOT / "outputs" / f"{stem}_review_report.md"
    json_path = PROJECT_ROOT / "outputs" / f"{stem}_review_report.json"

    md_path.parent.mkdir(parents=True, exist_ok=True)

    md_path.write_text(markdown_report, encoding="utf-8")
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    console.print(
        Panel.fit(
            f"[bold]File:[/bold] {loaded['file_name']}\n"
            f"[bold]Predicted Contract Type:[/bold] {classification['contract_type']}\n"
            f"[bold]Confidence:[/bold] {classification['confidence']:.2f}\n"
            f"[bold]Clauses Reviewed:[/bold] {len(clauses)}\n"
            f"[bold]Markdown Report:[/bold] {md_path}\n"
            f"[bold]JSON Report:[/bold] {json_path}",
            title="Review Report Generated",
        )
    )

    table = Table(title="Flag Counts")
    table.add_column("Flag", style="cyan")
    table.add_column("Count", justify="right", style="green")

    for flag, count in payload["flag_counts"].items():
        table.add_row(flag, str(count))

    console.print(table)


if __name__ == "__main__":
    main()