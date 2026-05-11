from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ingest.document_loader import DocumentLoader
from preprocess.clause_segmenter import ClauseSegmenter
from classify.contract_classifier import ContractClassifier


console = Console()


def main():
    """
    Command-line test for document ingestion, contract type recognition,
    and clause segmentation.

    Usage:
        python src/main.py data/sample_contracts/sample_contract.txt
    """

    import sys

    if len(sys.argv) < 2:
        console.print("[red]Please provide a file path.[/red]")
        console.print("Example:")
        console.print("python src/main.py data/sample_contracts/sample_contract.txt")
        return

    file_path = sys.argv[1]

    loader = DocumentLoader()
    classifier = ContractClassifier()
    segmenter = ClauseSegmenter()

    try:
        result = loader.load(file_path)
        classification = classifier.classify(result["text"], source_file=result["file_name"])
        clauses = segmenter.segment(result["text"])

        console.print(
            Panel.fit(
                f"[bold]File Name:[/bold] {result['file_name']}\n"
                f"[bold]File Type:[/bold] {result['file_type']}\n"
                f"[bold]Text Length:[/bold] {len(result['text'])} characters",
                title="Document Loaded Successfully",
            )
        )

        console.print(
            Panel.fit(
                f"[bold]Predicted Contract Type:[/bold] {classification['contract_type']}\n"
                f"[bold]Confidence:[/bold] {classification['confidence']:.2f}\n"
                f"[bold]Matched Keywords:[/bold] {', '.join(classification['matched_keywords']) or 'None'}",
                title="Contract Type Recognition",
            )
        )

        table = Table(title="Detected Clauses")
        table.add_column("Clause No.", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("Text Preview", style="white")

        for clause in clauses:
            preview = clause["text"][:120].replace("\n", " ")
            table.add_row(
                clause["clause_number"],
                clause["title"],
                preview,
            )

        console.print(table)

        console.print(
            Panel.fit(
                f"[bold]Total Clauses Detected:[/bold] {len(clauses)}",
                title="Pipeline Progress",
            )
        )

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()
