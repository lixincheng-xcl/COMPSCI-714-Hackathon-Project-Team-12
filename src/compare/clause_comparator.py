import re
from typing import Dict, List, Optional


class ClauseComparator:
    """
    Compare an uploaded contract clause with retrieved UoA reference material.

    This MVP comparator uses rule-based risk indicators and retrieval evidence
    to assign Green / Amber / Red / Blue flags.

    It does not provide legal advice. It only provides review-support signals.
    """

    HIGH_RISK_PATTERNS = {
        "Confidentiality": [
            r"\bindefinite\b",
            r"\bperpetual\b",
            r"\bforever\b",
            r"\bwithout exception\b",
            r"\bno exception\b",
        ],
        "Intellectual Property": [
            r"\bassigns? all\b.*\bintellectual property\b",
            r"\bexclusive ownership\b",
            r"\bowned exclusively by\b",
            r"\buniversity assigns\b",
            r"\ball results.*owned by\b",
        ],
        "Publication": [
            r"\bno publication\b",
            r"\bmust not publish\b",
            r"\bprior written approval\b",
            r"\bapproval before publication\b",
            r"\bembargo\b.*\b(1[3-9]|[2-9][0-9])\s*months\b",
        ],
        "Liability": [
            r"\bunlimited liability\b",
            r"\bindemnif(?:y|ies|ication)\b",
            r"\bconsequential loss\b",
            r"\bindirect loss\b",
            r"\bliable for all\b",
        ],
        "Termination": [
            r"\bno right to terminate\b",
            r"\bmay not terminate\b",
            r"\btermination only by\b.*\bpartner\b",
        ],
        "Governing Law": [
            r"\blaws of (?!new zealand)[a-z ]+\b",
            r"\bjurisdiction of (?!the courts of new zealand)[a-z ]+\b",
        ],
    }

    REVIEW_TERMS = {
        "Confidentiality": ["confidential", "disclose", "consent", "secure"],
        "Intellectual Property": ["intellectual property", "ip", "ownership", "licence", "results"],
        "Publication": ["publish", "publication", "review period", "research outcomes"],
        "Liability": ["liability", "responsible", "acts", "omissions", "loss"],
        "Termination": ["terminate", "termination", "notice"],
        "Governing Law": ["governed", "laws of new zealand", "jurisdiction"],
    }

    def compare(
        self,
        clause: Dict[str, str],
        matches: List[Dict[str, object]],
    ) -> Dict[str, object]:
        """
        Compare one clause against retrieved references and assign a review flag.

        Args:
            clause: A clause dictionary from ClauseSegmenter.
            matches: Retrieved reference matches from ReferenceRetriever.

        Returns:
            A structured comparison result.
        """
        clause_text = clause.get("text", "")
        clause_title = clause.get("title", "")
        query_topic = matches[0].get("query_topic", "Unknown") if matches else self._infer_topic(clause_title)

        if not matches:
            return self._result(
                clause=clause,
                topic=query_topic,
                flag="Blue",
                alignment="No reference found",
                confidence="Low",
                rationale="No relevant UoA reference material was retrieved for this clause. Human review is required.",
                reference=None,
                risk_indicators=[],
            )

        top_match = matches[0]
        risk_indicators = self._detect_high_risk_terms(query_topic, clause_text)

        if risk_indicators:
            return self._result(
                clause=clause,
                topic=query_topic,
                flag="Red",
                alignment="Potential conflict or high-risk deviation",
                confidence="Medium",
                rationale=(
                    "The clause contains high-risk wording that may conflict with a standard university position. "
                    "This should be escalated for human review."
                ),
                reference=top_match,
                risk_indicators=risk_indicators,
            )

        top_score = float(top_match.get("score", 0.0))
        chunk_topic = top_match.get("chunk_topic", "Unknown")
        reference_type = top_match.get("reference_type", "")
        matched_terms = top_match.get("matched_terms", [])

        topic_aligned = query_topic != "Unknown" and query_topic == chunk_topic
        has_key_terms = self._has_key_terms(query_topic, clause_text)

        if topic_aligned and top_score >= 6.0 and has_key_terms:
            flag = "Green"
            alignment = "Appears aligned with retrieved UoA reference"
            confidence = "Medium"
            rationale = (
                "The clause topic matches the retrieved reference topic and contains expected clause-level terms. "
                "No obvious high-risk wording was detected by the MVP rule checks."
            )

        elif topic_aligned and top_score >= 4.0:
            flag = "Amber"
            alignment = "Partially aligned but requires review"
            confidence = "Medium"
            rationale = (
                "A relevant UoA reference was retrieved, but the clause should still be reviewed because the MVP "
                "comparison is based on lexical and rule-based signals only."
            )

        elif reference_type == "contracting_position":
            flag = "Amber"
            alignment = "Relevant policy position found"
            confidence = "Medium"
            rationale = (
                "The system retrieved a relevant contracting position. Human review is required to confirm whether "
                "the uploaded clause follows the preferred or acceptable position."
            )

        else:
            flag = "Blue"
            alignment = "Reference coverage uncertain"
            confidence = "Low"
            rationale = (
                "The system could not confidently match this clause to a clearly aligned UoA reference. "
                "This may indicate missing coverage or a need for manual interpretation."
            )

        return self._result(
            clause=clause,
            topic=query_topic,
            flag=flag,
            alignment=alignment,
            confidence=confidence,
            rationale=rationale,
            reference=top_match,
            risk_indicators=risk_indicators,
            matched_terms=matched_terms,
        )

    def _detect_high_risk_terms(self, topic: str, text: str) -> List[str]:
        patterns = self.HIGH_RISK_PATTERNS.get(topic, [])
        lower_text = text.lower()

        indicators = []
        for pattern in patterns:
            if re.search(pattern, lower_text):
                indicators.append(pattern)

        return indicators

    def _has_key_terms(self, topic: str, text: str) -> bool:
        terms = self.REVIEW_TERMS.get(topic, [])
        normalised_text = self._normalise(text)
        return any(self._normalise(term) in normalised_text for term in terms)

    def _infer_topic(self, title: str) -> str:
        title_norm = self._normalise(title)

        for topic in self.REVIEW_TERMS:
            if self._normalise(topic) in title_norm:
                return topic

        return "Unknown"

    def _normalise(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _result(
        self,
        clause: Dict[str, str],
        topic: str,
        flag: str,
        alignment: str,
        confidence: str,
        rationale: str,
        reference: Optional[Dict[str, object]],
        risk_indicators: List[str],
        matched_terms: Optional[List[str]] = None,
    ) -> Dict[str, object]:
        return {
            "clause_number": clause.get("clause_number", "N/A"),
            "clause_title": clause.get("title", ""),
            "clause_text": clause.get("text", ""),
            "topic": topic,
            "flag": flag,
            "alignment": alignment,
            "confidence": confidence,
            "rationale": rationale,
            "risk_indicators": risk_indicators,
            "matched_terms": matched_terms or [],
            "reference": {
                "source_file": reference.get("source_file", "") if reference else "",
                "reference_type": reference.get("reference_type", "") if reference else "",
                "contract_type_hint": reference.get("contract_type_hint", "") if reference else "",
                "chunk_topic": reference.get("chunk_topic", "") if reference else "",
                "score": reference.get("score", 0.0) if reference else 0.0,
                "snippet": reference.get("snippet", "") if reference else "",
            },
            "human_review_required": True,
        }
