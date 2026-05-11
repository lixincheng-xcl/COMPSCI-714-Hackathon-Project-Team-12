from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from retrieve.reference_loader import ReferenceLoader


console = Console()


def main():
    loader = ReferenceLoader()
    references = loader.load_references()

    console.print(
        Panel.fit(
            f"[bold]Total References Loaded:[/bold] {len(references)}",
            title="Reference Loading Completed",
        )
    )

    table = Table(title="Loaded Reference Documents")
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Contract Type Hint", style="yellow")
    table.add_column("Direction", style="magenta")
    table.add_column("Source File", style="white")
    table.add_column("Text Length", justify="right")

    for idx, ref in enumerate(references, start=1):
        table.add_row(
            str(idx),
            ref.get("reference_type", ""),
            ref.get("contract_type_hint", ""),
            ref.get("direction_hint", ""),
            ref.get("source_file", ""),
            str(ref.get("text_length", 0)),
        )

    console.print(table)

    errors = [ref for ref in references if ref.get("error")]
    if errors:
        console.print("[red]Some files could not be loaded:[/red]")
        for ref in errors:
            console.print(f"- {ref['source_file']}: {ref['error']}")


if __name__ == "__main__":
    main()
