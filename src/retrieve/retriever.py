import math
import re
from typing import Dict, List, Optional, Set

from retrieve.reference_loader import ReferenceLoader


class ReferenceRetriever:
    """
    Lexical reference retriever for the Research Contract Adviser Agent.

    This retriever loads UoA reference templates and contracting position documents,
    chunks them into searchable blocks, detects clause topics, and retrieves the most
    relevant reference chunks for a given contract clause.

    It is intentionally lightweight for MVP use. Later it can be replaced or enhanced
    with embeddings, Azure AI Search, or Microsoft Foundry retrieval.
    """

    STOPWORDS = {
        "the", "a", "an", "and", "or", "of", "to", "in", "for", "by", "on",
        "with", "as", "is", "are", "be", "this", "that", "it", "its", "from",
        "at", "will", "shall", "may", "must", "under", "between", "each",
        "party", "parties", "agreement", "contract", "clause", "section",
        "university", "auckland", "research"
    }

    TOPIC_KEYWORDS: Dict[str, List[str]] = {
        "Parties": [
            "parties", "party", "university of auckland", "collaborator",
            "provider", "recipient", "client"
        ],
        "Confidentiality": [
            "confidentiality", "confidential", "confidential information",
            "disclose", "disclosure", "non disclosure", "nda", "cda",
            "third parties", "written consent"
        ],
        "Intellectual Property": [
            "intellectual property", "ip", "background ip", "project ip",
            "results", "invention", "ownership", "licence", "license",
            "commercialisation", "commercialization"
        ],
        "Publication": [
            "publication", "publish", "academic publication", "review period",
            "manuscript", "research outcomes", "publications"
        ],
        "Liability": [
            "liability", "liable", "indemnity", "indemnify", "loss",
            "damage", "damages", "limitation of liability", "acts and omissions"
        ],
        "Termination": [
            "termination", "terminate", "terminated", "notice", "expiry",
            "breach", "immediate termination"
        ],
        "Governing Law": [
            "governing law", "laws of new zealand", "new zealand law",
            "jurisdiction", "courts of new zealand", "dispute"
        ],
        "Data Use": [
            "data", "personal data", "dataset", "privacy", "access data",
            "data transfer", "data access"
        ],
        "Material Transfer": [
            "material", "materials", "biological material", "material transfer",
            "provider material", "recipient material"
        ],
        "Payment": [
            "payment", "fee", "fees", "invoice", "funding", "budget",
            "cost", "payable"
        ],
    }

    def __init__(self, references: Optional[List[Dict[str, object]]] = None):
        self.references = references if references is not None else ReferenceLoader().load_references()
        self.index = self._build_index(self.references)

    def retrieve(
        self,
        query: str,
        contract_type: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, object]]:
        """
        Retrieve the most relevant reference chunks for a query clause.
        """
        query_tokens = self._tokenise(query)
        query_topic = self._detect_topic(query)

        if not query_tokens:
            return []

        results = []

        for item in self.index:
            score, matched_terms, score_details = self._score(
                query_tokens=query_tokens,
                query_topic=query_topic,
                chunk_tokens=item["tokens"],
                chunk_text=item["text"],
                chunk_topic=item["topic"],
                contract_type=contract_type,
                reference_contract_type=item["contract_type_hint"],
                reference_type=item["reference_type"],
            )

            if score > 0:
                results.append(
                    {
                        "score": round(score, 4),
                        "query_topic": query_topic,
                        "chunk_topic": item["topic"],
                        "matched_terms": sorted(matched_terms),
                        "score_details": score_details,
                        "reference_type": item["reference_type"],
                        "contract_type_hint": item["contract_type_hint"],
                        "direction_hint": item["direction_hint"],
                        "source_file": item["source_file"],
                        "chunk_id": item["chunk_id"],
                        "text": item["text"],
                        "snippet": self._make_snippet(item["text"], focus_terms=list(matched_terms) + self.TOPIC_KEYWORDS.get(query_topic, [])),
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def _build_index(self, references: List[Dict[str, object]]) -> List[Dict[str, object]]:
        index = []

        for ref in references:
            text = ref.get("text", "")
            if not text:
                continue

            chunks = self._chunk_text(text)

            for i, chunk in enumerate(chunks):
                index.append(
                    {
                        "reference_type": ref.get("reference_type", ""),
                        "contract_type_hint": ref.get("contract_type_hint", ""),
                        "direction_hint": ref.get("direction_hint", ""),
                        "source_file": ref.get("source_file", ""),
                        "chunk_id": i,
                        "text": chunk,
                        "tokens": self._tokenise(chunk),
                        "topic": self._detect_topic(chunk),
                    }
                )

        return index

    def _chunk_text(self, text: str, max_chars: int = 1000) -> List[str]:
        """
        Split reference documents into smaller chunks.

        The current DOCX extraction may flatten some headings, so this function
        uses both paragraph breaks and fallback character-based splitting.
        """
        text = text.replace("\r\n", "\n")
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

        chunks = []
        current = ""

        for paragraph in paragraphs:
            if len(current) + len(paragraph) + 2 <= max_chars:
                current = f"{current}\n\n{paragraph}".strip()
            else:
                if current:
                    chunks.append(current)
                current = paragraph

        if current:
            chunks.append(current)

        # Fallback for documents with very few paragraph breaks
        if len(chunks) <= 2 and len(text) > max_chars:
            chunks = []
            step = int(max_chars * 0.75)
            for start in range(0, len(text), step):
                chunks.append(text[start:start + max_chars])

        return chunks

    def _score(
        self,
        query_tokens: Set[str],
        query_topic: str,
        chunk_tokens: Set[str],
        chunk_text: str,
        chunk_topic: str,
        contract_type: Optional[str],
        reference_contract_type: str,
        reference_type: str,
    ):
        overlap = query_tokens.intersection(chunk_tokens)

        if not overlap:
            return 0.0, set(), {}

        matched_terms = set(overlap)

        # Base lexical overlap score
        lexical_score = len(overlap) / math.sqrt(len(query_tokens) + 1)

        # Topic match is very important for clause-level retrieval
        topic_score = 0.0
        if query_topic != "Unknown":
            if query_topic == chunk_topic:
                topic_score = 4.0
            elif self._topic_terms_overlap(query_topic, chunk_text):
                topic_score = 2.5

        # Prefer references from the same contract type, but do not let this dominate
        contract_score = 0.0
        if contract_type and reference_contract_type:
            if contract_type.lower() == reference_contract_type.lower():
                contract_score = 1.0
            elif contract_type.lower() in reference_contract_type.lower():
                contract_score = 0.5
            elif reference_contract_type.lower() in contract_type.lower():
                contract_score = 0.5

        # Contracting positions are important but not always clause-specific
        position_score = 0.7 if reference_type == "contracting_position" else 0.0

        # Exact phrase bonus for important clause terms
        phrase_score = self._phrase_bonus(query_topic, chunk_text)

        total = lexical_score + topic_score + contract_score + position_score + phrase_score

        details = {
            "lexical_score": round(lexical_score, 4),
            "topic_score": round(topic_score, 4),
            "contract_score": round(contract_score, 4),
            "position_score": round(position_score, 4),
            "phrase_score": round(phrase_score, 4),
        }

        return total, matched_terms, details

    def _detect_topic(self, text: str) -> str:
        """
        Detect the dominant clause topic.

        The clause title or early text should be treated as stronger evidence than
        generic words appearing later in the clause. This avoids cases where
        "Intellectual Property" is misclassified as "Parties" simply because the
        clause text contains the word "parties".
        """
        normalised = self._normalise(text)
        first_part = normalised[:300]

        best_topic = "Unknown"
        best_score = 0.0

        for topic, keywords in self.TOPIC_KEYWORDS.items():
            topic_norm = self._normalise(topic)
            score = 0.0

            # Strongest signal: exact topic name appears near the beginning.
            if topic != "Parties" and topic_norm in first_part:
                score += 10.0
            elif topic == "Parties" and topic_norm in first_part:
                score += 4.0

            for keyword in keywords:
                kw = self._normalise(keyword)
                if not kw:
                    continue

                is_phrase = len(kw.split()) >= 2

                if kw in first_part:
                    score += 3.0 if is_phrase else 0.8
                elif kw in normalised:
                    score += 1.5 if is_phrase else 0.2

            # "Parties" is a generic topic and should not dominate specialist clauses.
            if topic == "Parties":
                score *= 0.45

            if score > best_score:
                best_topic = topic
                best_score = score

        return best_topic if best_score >= 1.0 else "Unknown"

    def _topic_terms_overlap(self, topic: str, text: str) -> bool:
        normalised = self._normalise(text)
        keywords = self.TOPIC_KEYWORDS.get(topic, [])
        return any(self._normalise(keyword) in normalised for keyword in keywords)

    def _phrase_bonus(self, topic: str, chunk_text: str) -> float:
        normalised = self._normalise(chunk_text)
        keywords = self.TOPIC_KEYWORDS.get(topic, [])

        bonus = 0.0
        for keyword in keywords:
            kw = self._normalise(keyword)
            if len(kw.split()) >= 2 and kw in normalised:
                bonus += 0.8

        return min(bonus, 2.4)

    def _tokenise(self, text: str) -> Set[str]:
        text = self._normalise(text)
        words = re.findall(r"[a-z][a-z0-9]{2,}", text)
        return {w for w in words if w not in self.STOPWORDS}

    def _normalise(self, text: str) -> str:
        text = text.lower()
        text = text.replace("_", " ")
        text = text.replace("-", " ")
        text = text.replace("/", " ")
        text = text.replace("\\", " ")
        text = re.sub(r"[^a-z0-9]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _make_snippet(self, text: str, max_length: int = 300, focus_terms=None) -> str:
        """
        Create a readable snippet. If focus terms are available, show the text
        around the first relevant term instead of always showing the beginning.
        """
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) <= max_length:
            return text

        focus_terms = focus_terms or []
        lower_text = text.lower()

        for term in sorted(focus_terms, key=len, reverse=True):
            if not term or len(term) < 3:
                continue

            term_lower = str(term).lower()
            pos = lower_text.find(term_lower)

            if pos >= 0:
                start = max(0, pos - 80)
                end = min(len(text), start + max_length)

                # Keep snippet length stable when focus term is near the end.
                start = max(0, end - max_length)

                prefix = "..." if start > 0 else ""
                suffix = "..." if end < len(text) else ""

                return prefix + text[start:end].strip() + suffix

        return text[:max_length].rstrip() + "..."
