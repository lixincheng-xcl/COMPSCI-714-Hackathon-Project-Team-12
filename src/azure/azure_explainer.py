import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


class AzureExplainer:
    """
    Azure-powered explanation enhancer.

    This component does not decide the review flag.
    It only rewrites the existing local rule-based rationale into a clearer
    human-review note grounded in the clause and retrieved reference.
    """

    def __init__(self, timeout_seconds: int = 20):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.base_url = os.getenv("AZURE_OPENAI_BASE_URL")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.timeout_seconds = timeout_seconds

        if not self.api_key:
            raise RuntimeError("Missing AZURE_OPENAI_API_KEY")

        if not self.base_url:
            raise RuntimeError("Missing AZURE_OPENAI_BASE_URL")

        if not self.deployment:
            raise RuntimeError("Missing AZURE_OPENAI_DEPLOYMENT")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout_seconds,
            max_retries=0,
        )

    def enhance(self, comparison: Dict[str, object]) -> str:
        """
        Generate a clearer explanation for a clause-level review result.

        Args:
            comparison: Clause comparison result from ClauseComparator.

        Returns:
            Enhanced review rationale as plain text.
        """
        clause_number = comparison.get("clause_number", "")
        clause_title = comparison.get("clause_title", "")
        clause_text = comparison.get("clause_text", "")
        flag = comparison.get("flag", "")
        topic = comparison.get("topic", "")
        alignment = comparison.get("alignment", "")
        local_rationale = comparison.get("rationale", "")
        risk_indicators = comparison.get("risk_indicators", [])
        reference = comparison.get("reference", {})

        source_file = reference.get("source_file", "")
        reference_snippet = reference.get("snippet", "")

        prompt = f"""
You are assisting with an academic proof-of-concept contract review tool.

Important rules:
- Do not provide legal advice.
- Do not approve or reject the contract.
- Do not change the assigned flag.
- Do not invent facts not present in the clause or reference.
- Explain that human review is required.
- Write in clear professional English.

Clause number: {clause_number}
Clause title: {clause_title}
Detected topic: {topic}
Assigned flag: {flag}
Alignment: {alignment}

Uploaded clause text:
{clause_text}

Retrieved reference source:
{source_file}

Retrieved reference snippet:
{reference_snippet}

Local rule-based rationale:
{local_rationale}

Detected risk indicators:
{risk_indicators}

Write a concise enhanced rationale in 3 to 5 sentences.
"""

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write concise review-support explanations. "
                        "You do not provide legal advice."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=220,
        )

        return response.choices[0].message.content.strip()