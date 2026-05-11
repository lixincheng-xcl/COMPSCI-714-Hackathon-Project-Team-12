from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ingest.document_loader import DocumentLoader
from preprocess.clause_segmenter import ClauseSegmenter
from classify.contract_classifier import ContractClassifier
from retrieve.retriever import ReferenceRetriever


console = Console()


def main():
    """
    Test document loading, contract classification, clause segmentation,
    and reference retrieval together.

    Usage:
        python src/test_retrieval.py data/sample_contracts/sample_contract.txt
    """

    import sys

    if len(sys.argv) < 2:
        console.print("[red]Please provide a contract file path.[/red]")
        console.print("Example:")
        console.print("python src/test_retrieval.py data/sample_contracts/sample_contract.txt")
        return

    file_path = sys.argv[1]

    loader = DocumentLoader()
    classifier = ContractClassifier()
    segmenter = ClauseSegmenter()
    retriever = ReferenceRetriever()

    loaded = loader.load(file_path)
    classification = classifier.classify(
        loaded["text"],
        source_file=loaded["file_name"],
    )
    clauses = segmenter.segment(loaded["text"])

    console.print(
        Panel.fit(
            f"[bold]File:[/bold] {loaded['file_name']}\n"
            f"[bold]Predicted Contract Type:[/bold] {classification['contract_type']}\n"
            f"[bold]Clauses Detected:[/bold] {len(clauses)}\n"
            f"[bold]Reference Chunks Indexed:[/bold] {len(retriever.index)}",
            title="Retrieval Test Setup",
        )
    )

    for clause in clauses:
        query = f"{clause['title']}\n{clause['text']}"
        matches = retriever.retrieve(
            query=query,
            contract_type=classification["contract_type"],
            top_k=3,
        )

        query_topic = matches[0]["query_topic"] if matches else "Unknown"

        console.print(
            Panel.fit(
                f"[bold]Clause {clause['clause_number']}:[/bold] {clause['title']}\n"
                f"[bold]Query Topic:[/bold] {query_topic}\n"
                f"{clause['text'][:300]}",
                title="Input Clause",
            )
        )

        table = Table(title="Top Retrieved References")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Score", style="green", no_wrap=True)
        table.add_column("Chunk Topic", style="blue")
        table.add_column("Reference Type", style="yellow")
        table.add_column("Contract Type Hint", style="magenta")
        table.add_column("Source File", style="white")
        table.add_column("Matched Terms", style="white")
        table.add_column("Snippet", style="white")

        for rank, match in enumerate(matches, start=1):
            matched_terms = ", ".join(match.get("matched_terms", [])[:6])
            table.add_row(
                str(rank),
                str(match["score"]),
                match.get("chunk_topic", ""),
                match["reference_type"],
                match["contract_type_hint"],
                match["source_file"],
                matched_terms,
                match["snippet"][:160],
            )

        console.print(table)


if __name__ == "__main__":
    main()
