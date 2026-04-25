from rich.console import Console
from rich.panel import Panel

from ingest.document_loader import DocumentLoader


console = Console()


def main():
    """
    Simple command-line test for document ingestion.

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

    try:
        result = loader.load(file_path)

        console.print(
            Panel.fit(
                f"[bold]File Name:[/bold] {result['file_name']}\n"
                f"[bold]File Type:[/bold] {result['file_type']}\n"
                f"[bold]Text Length:[/bold] {len(result['text'])} characters",
                title="Document Loaded Successfully",
            )
        )

        preview = result["text"][:1500]

        console.print(
            Panel(
                preview,
                title="Extracted Text Preview",
                subtitle="First 1500 characters",
            )
        )

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()
