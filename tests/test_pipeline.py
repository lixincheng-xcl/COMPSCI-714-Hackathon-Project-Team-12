import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ingest.document_loader import DocumentLoader
from preprocess.clause_segmenter import ClauseSegmenter
from classify.contract_classifier import ContractClassifier
from retrieve.reference_loader import ReferenceLoader
from retrieve.retriever import ReferenceRetriever
from report.report_generator import ReportGenerator
from pipeline.review_pipeline import ReviewPipeline


SAFE_SAMPLE = PROJECT_ROOT / "data" / "sample_contracts" / "sample_contract.txt"
RISKY_SAMPLE = PROJECT_ROOT / "data" / "sample_contracts" / "risky_contract.txt"


def test_document_loader_loads_safe_sample():
    loader = DocumentLoader()
    loaded = loader.load(str(SAFE_SAMPLE))

    assert loaded["file_name"] == "sample_contract.txt"
    assert loaded["file_type"] == ".txt"
    assert "RESEARCH COLLABORATION AGREEMENT" in loaded["text"]
    assert len(loaded["text"]) > 100


def test_clause_segmenter_detects_seven_clauses():
    loader = DocumentLoader()
    segmenter = ClauseSegmenter()

    loaded = loader.load(str(SAFE_SAMPLE))
    clauses = segmenter.segment(loaded["text"])

    assert len(clauses) == 7
    assert clauses[0]["clause_number"] == "1"
    assert clauses[0]["title"] == "Parties"
    assert clauses[1]["title"] == "Confidentiality"
    assert clauses[2]["title"] == "Intellectual Property"


def test_contract_classifier_identifies_safe_sample():
    loader = DocumentLoader()
    classifier = ContractClassifier()

    loaded = loader.load(str(SAFE_SAMPLE))
    classification = classifier.classify(
        loaded["text"],
        source_file=loaded["file_name"],
    )

    assert classification["contract_type"] == "Research Collaboration Agreement"
    assert classification["confidence"] > 0.5


def test_reference_loader_loads_reference_documents():
    loader = ReferenceLoader()
    references = loader.load_references()

    assert len(references) >= 15

    source_files = [ref["source_file"] for ref in references]

    assert any("Research Collaboration Agreement" in name for name in source_files)
    assert any("Contracting Positions" in name for name in source_files)


def test_reference_retriever_returns_matches():
    retriever = ReferenceRetriever()

    matches = retriever.retrieve(
        query="Confidentiality\nEach party must keep confidential information secure.",
        contract_type="Research Collaboration Agreement",
        top_k=3,
    )

    assert len(matches) > 0
    assert matches[0]["score"] > 0
    assert matches[0]["source_file"]


def test_review_pipeline_safe_sample_outputs_expected_flags():
    pipeline = ReviewPipeline()
    output = pipeline.run(str(SAFE_SAMPLE))

    classification = output["classification"]
    clauses = output["clauses"]
    payload = output["payload"]

    assert classification["contract_type"] == "Research Collaboration Agreement"
    assert classification["confidence"] > 0.5
    assert len(clauses) == 7

    assert payload["flag_counts"]["Red"] == 0
    assert payload["flag_counts"]["Blue"] == 0
    assert payload["flag_counts"]["Green"] >= 4
    assert payload["flag_counts"]["Amber"] >= 1


def test_review_pipeline_risky_sample_outputs_red_flags():
    pipeline = ReviewPipeline()
    output = pipeline.run(str(RISKY_SAMPLE))

    classification = output["classification"]
    clauses = output["clauses"]
    payload = output["payload"]

    assert classification["contract_type"] == "Research Collaboration Agreement"
    assert classification["confidence"] > 0.5
    assert len(clauses) == 7

    assert payload["flag_counts"]["Red"] >= 5
    assert payload["flag_counts"]["Green"] == 0


def test_report_generator_outputs_markdown_from_pipeline_payload():
    pipeline = ReviewPipeline()
    output = pipeline.run(str(SAFE_SAMPLE))

    payload = output["payload"]

    generator = ReportGenerator()
    markdown = generator.to_markdown(payload)

    assert "Research Contract Adviser Agent - Review Report" in markdown
    assert "Green Flags" in markdown
    assert "Amber Flags" in markdown
    assert "Red Flags" in markdown
    assert "Blue Flags" in markdown
    assert payload["total_clauses_reviewed"] == 7