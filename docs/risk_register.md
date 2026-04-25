# Risk Register

## 1. Purpose

This document records key risks and mitigation strategies for the Research Contract Adviser Agent.

## 2. Risk Register

| Risk | Description | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| Confidentiality risk | Contract documents may contain sensitive or commercial information | High | Medium | Use anonymised or synthetic documents only |
| Hallucination risk | The system may generate unsupported explanations | High | Medium | Ground outputs in retrieved references and include evidence |
| Incorrect flagging | Clauses may be wrongly classified as Green / Amber / Red / Blue | High | Medium | Keep human review mandatory and test against benchmark cases |
| Over-automation risk | Users may treat the system as a legal decision-maker | High | Medium | Add disclaimers and human-in-the-loop reminders |
| Data leakage | Sensitive files or API keys may be committed to GitHub | High | Low | Use .gitignore and avoid storing private data in the repo |
| Poor retrieval quality | Relevant reference clauses may not be retrieved | Medium | Medium | Evaluate retrieval results and improve indexing |
| Lack of explainability | Users may not understand why a flag was generated | Medium | Medium | Provide clause, reference, flag, and rationale in the report |

## 3. Governance Principles

- The system does not provide legal advice.
- The system does not approve contracts.
- The system supports human review only.
- Every output should be explainable and traceable.
- Confidential data must not be uploaded to public repositories.
