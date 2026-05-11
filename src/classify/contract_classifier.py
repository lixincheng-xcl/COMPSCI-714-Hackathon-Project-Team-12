import re
from typing import Dict, List, Tuple


class ContractClassifier:
    """
    Rule-based contract type recogniser for the Research Contract Adviser Agent.

    This MVP classifier combines:
    1. strong filename/title signals;
    2. early-document heading signals;
    3. weaker full-text keyword signals.

    This is more reliable than simple keyword counting because many contract templates
    contain overlapping legal terms such as confidentiality, NDA, data, liability, etc.
    """

    CONTRACT_TYPE_KEYWORDS: Dict[str, List[str]] = {
        "Research Collaboration Agreement": [
            "research collaboration agreement",
            "collaboration agreement",
            "collaborative research",
            "research partner",
            "collaborator",
        ],
        "Material Transfer Agreement": [
            "material transfer agreement",
            "material transfer",
            "mta",
            "transfer of material",
            "materials transferred",
            "research material",
            "biological material",
            "provider material",
            "recipient material",
        ],
        "Data Transfer Agreement": [
            "data transfer agreement",
            "data transfer",
            "dta",
            "transfer of data",
            "dataset",
            "personal data",
        ],
        "Data Access Agreement": [
            "data access agreement",
            "data access",
            "access data",
            "access to data",
            "data held by",
        ],
        "Confidential Disclosure Agreement": [
            "confidential disclosure agreement",
            "non-disclosure agreement",
            "cda",
            "nda",
            "confidential information",
        ],
        "Research Subcontract": [
            "subcontractor agreement",
            "subcontract",
            "research subcontract",
            "subaward",
            "sub-contractor",
        ],
        "Research Services Agreement": [
            "research services agreement",
            "research services",
            "research service",
        ],
        "Provision of Services Agreement": [
            "provision of services agreement",
            "services agreement",
            "provide services",
        ],
        "Master Services Agreement": [
            "master services agreement",
            "statement of work",
            "services schedule",
        ],
        "Student Research Agreement": [
            "student research agreement",
            "student research project",
            "student project",
        ],
        "Research Contract": [
            "research contract",
            "research agreement",
            "sponsored research",
            "commercial research",
            "public research",
        ],
    }

    def classify(self, text: str, source_file: str = "") -> Dict[str, object]:
        """
        Classify contract type using weighted keyword matching.

        Args:
            text: Extracted contract text.
            source_file: Optional source filename. This is treated as a strong signal.

        Returns:
            A dictionary containing contract type, confidence score, matched keywords,
            and score details.
        """
        if not text or not text.strip():
            return {
                "contract_type": "Unknown",
                "confidence": 0.0,
                "matched_keywords": [],
                "score_details": {},
            }

        normalised_text = self._normalise(text)
        normalised_file = self._normalise(source_file)
        early_text = normalised_text[:2000]

        scores: List[Tuple[str, float, List[str], Dict[str, float]]] = []

        for contract_type, keywords in self.CONTRACT_TYPE_KEYWORDS.items():
            score = 0.0
            matched_keywords = []
            details = {
                "filename_score": 0.0,
                "early_text_score": 0.0,
                "full_text_score": 0.0,
            }

            for keyword in keywords:
                kw = self._normalise(keyword)

                # Strongest signal: filename
                if kw in normalised_file:
                    score += 6.0
                    details["filename_score"] += 6.0
                    matched_keywords.append(keyword)

                # Strong signal: first part of document, usually title / heading
                elif kw in early_text:
                    score += 3.0
                    details["early_text_score"] += 3.0
                    matched_keywords.append(keyword)

                # Weak signal: anywhere in full text
                elif kw in normalised_text:
                    score += 1.0
                    details["full_text_score"] += 1.0
                    matched_keywords.append(keyword)

            scores.append((contract_type, score, matched_keywords, details))

        scores.sort(key=lambda item: item[1], reverse=True)

        best_type, best_score, matched_keywords, details = scores[0]

        if best_score == 0:
            return {
                "contract_type": "Unknown",
                "confidence": 0.0,
                "matched_keywords": [],
                "score_details": details,
            }

        # Confidence is capped at 1.0. A score of 6 or above usually means filename/title match.
        confidence = min(1.0, best_score / 6.0)

        return {
            "contract_type": best_type,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "score_details": details,
        }

    def _normalise(self, value: str) -> str:
        """
        Normalise text so that filenames like 'Material_Transfer_Agreement'
        match phrases like 'material transfer agreement'.

        This implementation avoids regex character-range issues by replacing
        common filename separators before applying a general cleanup regex.
        """
        value = value.lower()
        value = value.replace("_", " ")
        value = value.replace("-", " ")
        value = value.replace("/", " ")
        value = value.replace("\\", " ")
        value = re.sub(r"[^a-z0-9]+", " ", value)
        value = re.sub(r"\s+", " ", value).strip()
        return value
