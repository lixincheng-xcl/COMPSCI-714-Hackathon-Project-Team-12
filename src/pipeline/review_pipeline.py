import os
import multiprocessing as mp
from typing import Dict, List, Optional

from dotenv import load_dotenv

from ingest.document_loader import DocumentLoader
from classify.contract_classifier import ContractClassifier
from preprocess.clause_segmenter import ClauseSegmenter
from retrieve.retriever import ReferenceRetriever
from compare.clause_comparator import ClauseComparator
from report.report_generator import ReportGenerator


load_dotenv()


def _azure_explainer_worker(comparison: Dict[str, object], queue: mp.Queue, timeout_seconds: int):
    """
    Run Azure explanation enhancement in a separate process.

    This prevents the main pipeline or Streamlit UI from hanging indefinitely
    if the Azure endpoint or network becomes slow.
    """
    try:
        from azure.azure_explainer import AzureExplainer

        explainer = AzureExplainer(timeout_seconds=timeout_seconds)
        enhanced = explainer.enhance(comparison)

        queue.put(
            {
                "ok": True,
                "text": enhanced,
                "error": "",
            }
        )

    except Exception as error:
        queue.put(
            {
                "ok": False,
                "text": "",
                "error": str(error),
            }
        )


class ReviewPipeline:
    """
    End-to-end review pipeline for the Research Contract Adviser Agent.

    Azure explanation enhancement is optional.
    Azure does not assign or change review flags.
    It only improves explanation readability based on local results and retrieved evidence.
    """

    def __init__(
        self,
        use_azure_explainer: bool = False,
        azure_flags_to_enhance: Optional[List[str]] = None,
        azure_max_explanations: int = 1,
        azure_call_timeout_seconds: int = 25,
    ):
        self.loader = DocumentLoader()
        self.classifier = ContractClassifier()
        self.segmenter = ClauseSegmenter()
        self.retriever = ReferenceRetriever()
        self.comparator = ClauseComparator()
        self.report_generator = ReportGenerator()

        env_enabled = os.getenv("AZURE_EXPLANATIONS_ENABLED", "false").lower() == "true"

        self.use_azure_explainer = use_azure_explainer and env_enabled
        self.azure_flags_to_enhance = azure_flags_to_enhance or ["Red"]
        self.azure_max_explanations = azure_max_explanations
        self.azure_call_timeout_seconds = azure_call_timeout_seconds

    def run(self, file_path: str) -> Dict[str, object]:
        loaded = self.loader.load(file_path)

        classification = self.classifier.classify(
            loaded["text"],
            source_file=loaded["file_name"],
        )

        clauses = self.segmenter.segment(loaded["text"])

        results: List[Dict[str, object]] = []
        azure_explanation_count = 0

        for clause in clauses:
            query = f"{clause['title']}\n{clause['text']}"

            matches = self.retriever.retrieve(
                query=query,
                contract_type=classification["contract_type"],
                top_k=5,
            )

            comparison = self.comparator.compare(clause, matches)

            should_enhance = (
                self.use_azure_explainer
                and comparison.get("flag") in self.azure_flags_to_enhance
                and azure_explanation_count < self.azure_max_explanations
            )

            if should_enhance:
                comparison = self._add_azure_explanation_with_timeout(comparison)

                if comparison.get("azure_explanation_used"):
                    azure_explanation_count += 1
            else:
                comparison["azure_enhanced_rationale"] = ""
                comparison["azure_explanation_used"] = False

            results.append(comparison)

        payload = self.report_generator.build_report_payload(
            file_name=loaded["file_name"],
            contract_type=classification["contract_type"],
            classification_confidence=classification["confidence"],
            results=results,
        )

        markdown_report = self.report_generator.to_markdown(payload)

        return {
            "loaded": loaded,
            "classification": classification,
            "clauses": clauses,
            "results": results,
            "payload": payload,
            "markdown_report": markdown_report,
            "azure_explanations_used": self.use_azure_explainer,
            "azure_explanation_count": azure_explanation_count,
        }

    def _add_azure_explanation_with_timeout(self, comparison: Dict[str, object]) -> Dict[str, object]:
        """
        Add Azure-enhanced rationale with a process-level timeout.

        If Azure is slow or unavailable, the pipeline falls back to the local rationale.
        This method does not change the original flag.
        """
        queue = mp.Queue()

        process = mp.Process(
            target=_azure_explainer_worker,
            args=(comparison, queue, self.azure_call_timeout_seconds),
        )

        process.start()
        process.join(self.azure_call_timeout_seconds + 5)

        if process.is_alive():
            process.terminate()
            process.join()

            comparison["azure_enhanced_rationale"] = ""
            comparison["azure_explanation_used"] = False
            comparison["azure_explanation_error"] = (
                f"Azure explanation timed out after {self.azure_call_timeout_seconds} seconds."
            )
            return comparison

        if queue.empty():
            comparison["azure_enhanced_rationale"] = ""
            comparison["azure_explanation_used"] = False
            comparison["azure_explanation_error"] = "Azure explanation failed without returning a result."
            return comparison

        result = queue.get()

        if result.get("ok"):
            comparison["azure_enhanced_rationale"] = result.get("text", "")
            comparison["azure_explanation_used"] = True
            comparison["azure_explanation_error"] = ""
        else:
            comparison["azure_enhanced_rationale"] = ""
            comparison["azure_explanation_used"] = False
            comparison["azure_explanation_error"] = result.get("error", "")

        return comparison