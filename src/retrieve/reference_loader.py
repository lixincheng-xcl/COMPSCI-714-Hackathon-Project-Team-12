from pathlib import Path
from typing import Dict, List

from ingest.document_loader import DocumentLoader


class ReferenceLoader:
    """
    Load UoA reference templates and contracting position documents.

    This module prepares the reference knowledge base for later retrieval,
    clause comparison, and flag generation.
    """

    def __init__(
        self,
        templates_dir: str = "data/reference_templates",
        positions_dir: str = "data/reference_positions",
    ):
        self.templates_dir = Path(templates_dir)
        self.positions_dir = Path(positions_dir)
        self.document_loader = DocumentLoader()

    def load_references(self) -> List[Dict[str, object]]:
        references = []

        references.extend(
            self._load_directory(
                directory=self.templates_dir,
                reference_type="template",
            )
        )

        references.extend(
            self._load_directory(
                directory=self.positions_dir,
                reference_type="contracting_position",
            )
        )

        return references

    def _load_directory(self, directory: Path, reference_type: str) -> List[Dict[str, object]]:
        if not directory.exists():
            return []

        supported_files = []
        for pattern in ("*.docx", "*.pdf", "*.txt"):
            supported_files.extend(directory.glob(pattern))

        references = []

        for file_path in sorted(supported_files):
            try:
                loaded = self.document_loader.load(str(file_path))
                text = loaded["text"]

                references.append(
                    {
                        "reference_id": self._make_reference_id(file_path),
                        "reference_type": reference_type,
                        "source_file": file_path.name,
                        "file_type": loaded["file_type"],
                        "contract_type_hint": self._infer_contract_type(file_path.name),
                        "direction_hint": self._infer_direction(file_path.name),
                        "text": text,
                        "text_length": len(text),
                    }
                )

            except Exception as e:
                references.append(
                    {
                        "reference_id": self._make_reference_id(file_path),
                        "reference_type": reference_type,
                        "source_file": file_path.name,
                        "file_type": file_path.suffix.lower(),
                        "contract_type_hint": "Unknown",
                        "direction_hint": "Unknown",
                        "text": "",
                        "text_length": 0,
                        "error": str(e),
                    }
                )

        return references

    def _make_reference_id(self, file_path: Path) -> str:
        return file_path.stem.lower().replace(" ", "_").replace("-", "_")

    def _infer_contract_type(self, filename: str) -> str:
        name = filename.lower()

        if "cda" in name or "confidential" in name:
            return "Confidential Disclosure Agreement"

        if "data transfer" in name:
            return "Data Transfer Agreement"

        if "data access" in name:
            return "Data Access Agreement"

        if "material_transfer" in name or "material transfer" in name or "mta" in name:
            return "Material Transfer Agreement"

        if "research collaboration" in name or "collaboration agreement" in name:
            return "Research Collaboration Agreement"

        if "research services" in name:
            return "Research Services Agreement"

        if "subcontract" in name or "subcontractor" in name:
            return "Research Subcontract"

        if "master services" in name:
            return "Master Services Agreement"

        if "student research" in name:
            return "Student Research Agreement"

        if "contracting positions" in name or "approvals and escalation" in name:
            return "UoA Contracting Positions"

        return "Unknown"

    def _infer_direction(self, filename: str) -> str:
        name = filename.lower()

        if "incoming" in name or "inbound" in name:
            return "Incoming"

        if "outgoing" in name or "outbound" in name:
            return "Outgoing"

        if "two way" in name or "two-way" in name:
            return "Two-way"

        return "Not specified"
