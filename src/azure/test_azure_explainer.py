import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.review_pipeline import ReviewPipeline
from azure.azure_explainer import AzureExplainer


console = Console()


def main():
    """
    Test Azure explanation enhancement on the risky sample contract.

    Usage:
        python src/azure/test_azure_explainer.py
    """

    sample_path = PROJECT_ROOT / "data" / "sample_contracts" / "risky_contract.txt"

    pipeline = ReviewPipeline()
    output = pipeline.run(str(sample_path))

    results = output["results"]

    red_results = [item for item in results if item["flag"] == "Red"]

    if not red_results:
        console.print("[red]No Red flag result found in risky sample.[/red]")
        return

    comparison = red_results[0]

    explainer = AzureExplainer()
    enhanced_rationale = explainer.enhance(comparison)

    console.print(
        Panel.fit(
            f"[bold]Clause:[/bold] {comparison['clause_number']} - {comparison['clause_title']}\n"
            f"[bold]Flag:[/bold] {comparison['flag']}\n"
            f"[bold]Original Rationale:[/bold]\n{comparison['rationale']}\n\n"
            f"[bold]Azure Enhanced Rationale:[/bold]\n{enhanced_rationale}",
            title="Azure Explanation Enhancer Test",
        )
    )


if __name__ == "__main__":
    main()