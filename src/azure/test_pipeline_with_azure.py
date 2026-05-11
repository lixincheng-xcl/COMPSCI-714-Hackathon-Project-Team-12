import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.review_pipeline import ReviewPipeline


console = Console()


def main():
    """
    Test the full review pipeline with Azure-enhanced explanations.

    Usage:
        python src/azure/test_pipeline_with_azure.py
    """

    sample_path = PROJECT_ROOT / "data" / "sample_contracts" / "risky_contract.txt"

    pipeline = ReviewPipeline(use_azure_explainer=True)
    output = pipeline.run(str(sample_path))

    results = output["results"]

    red_results = [item for item in results if item["flag"] == "Red"]

    if not red_results:
        console.print("[red]No Red flag result found.[/red]")
        return

    first_red = red_results[0]

    console.print(
        Panel.fit(
            f"[bold]Azure explanations used:[/bold] {output['azure_explanations_used']}\n"
            f"[bold]Clause:[/bold] {first_red['clause_number']} - {first_red['clause_title']}\n"
            f"[bold]Flag:[/bold] {first_red['flag']}\n\n"
            f"[bold]Local Rationale:[/bold]\n{first_red['rationale']}\n\n"
            f"[bold]Azure-Enhanced Rationale:[/bold]\n{first_red.get('azure_enhanced_rationale', '')}",
            title="Pipeline with Azure Explanation Test",
        )
    )


if __name__ == "__main__":
    main()