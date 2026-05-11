import re
from typing import Dict, List


class ClauseSegmenter:
    """
    Segment extracted contract text into structured clauses.

    This module takes plain contract text from DocumentLoader and converts it into
    a list of clause dictionaries.
    """

    CLAUSE_PATTERN = re.compile(
        r"(?m)^\s*(\d+(?:\.\d+)*)\.\s+(.+?)\s*$"
    )

    def segment(self, text: str) -> List[Dict[str, str]]:
        """
        Segment contract text into clauses.

        Args:
            text: Extracted contract text.

        Returns:
            A list of clause dictionaries.
        """
        if not text or not text.strip():
            return []

        matches = list(self.CLAUSE_PATTERN.finditer(text))

        if not matches:
            return [
                {
                    "clause_number": "N/A",
                    "title": "Full Document",
                    "text": text.strip(),
                }
            ]

        clauses = []

        for i, match in enumerate(matches):
            clause_number = match.group(1).strip()
            title = match.group(2).strip()

            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            clause_text = text[start:end].strip()

            clauses.append(
                {
                    "clause_number": clause_number,
                    "title": title,
                    "text": clause_text,
                }
            )

        return clauses