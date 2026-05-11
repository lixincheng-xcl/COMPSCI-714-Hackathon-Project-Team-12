# Checkpoint 2 - Solution Architecture and Implementation Progress

## Team 12 - NovaMind Collective  
## Use Case: Research Contract Adviser Agent

---

## 1. Project Overview

Our team is developing a proof-of-concept Research Contract Adviser Agent for supporting university staff in reviewing externally drafted research contracts.

The selected use case focuses on helping reviewers identify the likely contract type, compare contract clauses against UoA reference templates and contracting positions, detect possible deviations, and generate structured Green / Amber / Red / Blue review flags.

The system is designed as a human-in-the-loop review support tool. It does not provide legal advice, approve contracts, reject contracts, or replace professional contract managers or legal reviewers.

---

## 2. Problem Understanding

Research contracts are often reviewed manually against institutional templates and contracting positions. This process can be repetitive, time-consuming, and inconsistent, especially when different contract types contain similar but legally important clauses.

The main review challenges include:

- identifying the type of uploaded contract;
- finding relevant standard templates or contracting positions;
- comparing uploaded clauses against UoA preferred positions;
- detecting high-risk wording or deviations;
- producing a structured report that supports human decision-making.

Our interpretation of the problem is that this is not a general chatbot task. It is a document intelligence and decision-support task that requires grounded reference retrieval, clause-level comparison, and transparent reasoning.

---

## 3. Proposed Solution Architecture

Our solution follows a modular retrieval-augmented and rule-guided architecture.

The current pipeline is:

Document input  
→ Text extraction  
→ Contract type recognition  
→ Clause segmentation  
→ Reference document loading  
→ Reference retrieval  
→ Clause comparison  
→ Flag generation  
→ Markdown / JSON report generation  
→ Streamlit demo UI

This design was selected because contract review requires traceable outputs grounded in trusted reference materials, rather than unsupported free-form generation.

---

## 4. Implemented System Components

| Component | File | Description | Status |
|---|---|---|---|
| Document Loader | `src/ingest/document_loader.py` | Loads TXT, PDF, and DOCX files and extracts plain text. | Completed |
| Clause Segmenter | `src/preprocess/clause_segmenter.py` | Splits extracted contract text into structured clause objects. | Completed |
| Contract Classifier | `src/classify/contract_classifier.py` | Predicts the likely contract type using weighted keyword and filename signals. | Completed |
| Reference Loader | `src/retrieve/reference_loader.py` | Loads UoA templates and contracting position documents from local folders. | Completed |
| Reference Retriever | `src/retrieve/retriever.py` | Retrieves relevant reference chunks for each uploaded clause. | Completed |
| Clause Comparator / Flag Generator | `src/compare/clause_comparator.py` | Compares clauses with references and assigns Green / Amber / Red / Blue flags. | Completed |
| Report Generator | `src/report/report_generator.py` | Generates structured Markdown and JSON review reports. | Completed |
| Streamlit UI | `src/ui/app.py` | Provides a web-based demo interface for contract review. | Completed |
| Pipeline Tests | `tests/test_pipeline.py` | Tests the main pipeline modules and expected demo outputs. | Completed |

---

## 5. Reference Data and Knowledge Base

The current MVP uses reference materials provided through the course project package.

The local reference folders are:

- `data/reference_templates/`
- `data/reference_positions/`
- `docs/use_case/`

The reference knowledge base includes:

- UoA contract templates;
- UoA Contracting Positions and Approvals / Escalation Protocol;
- the Research Contract Adviser Agent use case brief.

These files are stored locally for development and demonstration. They should not be pushed to the public GitHub repository because they may contain internal course or institutional materials.

---

## 6. Flag Categories

The system generates four types of review flags:

| Flag | Meaning |
|---|---|
| Green | The clause appears aligned with retrieved UoA reference material. |
| Amber | The clause may be partially aligned, but human review is still required. |
| Red | The clause contains high-risk wording or a potential conflict with standard positions. |
| Blue | The system cannot confidently find relevant reference coverage. |

Each generated result includes:

- clause number;
- clause title;
- clause text;
- detected topic;
- review flag;
- rationale;
- retrieved reference source;
- reference snippet;
- human review requirement.

---

## 7. Current Demo Results

### Safe Sample Contract

Input:

`data/sample_contracts/sample_contract.txt`

Result:

| Flag | Count |
|---|---:|
| Red | 0 |
| Amber | 2 |
| Blue | 0 |
| Green | 5 |

This demonstrates that the system can identify generally acceptable clauses and classify most of them as Green while keeping uncertain clauses as Amber for human review.

### Risky Sample Contract

Input:

`data/sample_contracts/risky_contract.txt`

Result:

| Flag | Count |
|---|---:|
| Red | 6 |
| Amber | 1 |
| Blue | 0 |
| Green | 0 |

This demonstrates that the system can detect high-risk clauses involving confidentiality, intellectual property assignment, publication restrictions, unlimited liability, termination restrictions, and non-New Zealand governing law.

---

## 8. Testing Progress

The automated test suite currently passes:

8 passed in 4.17s

The tests cover:

- document loading;
- clause segmentation;
- contract type classification;
- reference document loading;
- reference retrieval;
- safe sample flag counts;
- risky sample red flag detection;
- Markdown / JSON report generation.

This provides evidence that the main MVP pipeline is functioning consistently.

---

## 9. User Interface Progress

A Streamlit demo interface has been implemented.

The UI supports:

- selecting a safe sample contract;
- selecting a risky sample contract;
- uploading TXT, PDF, or DOCX files;
- running the full contract review pipeline;
- displaying document summary information;
- displaying Red / Amber / Blue / Green flag counts;
- showing clause-level review details;
- downloading Markdown and JSON review reports.

The UI has been tested successfully using both safe and risky sample contracts.

---

## 10. Responsible AI and Governance Considerations

The system is designed with human oversight as a core requirement.

The system does not:

- provide legal advice;
- approve or reject contracts;
- replace contract managers or legal professionals;
- make final legal conclusions.

Important governance considerations include:

- confidential contract handling;
- avoiding upload of real non-anonymised contracts to public repositories;
- explaining why each flag was assigned;
- providing retrieved reference evidence;
- clearly stating that human review is required.

---

## 11. Current Limitations

The current MVP is functional but has several limitations:

- clause segmentation is rule-based and may not work perfectly for complex PDF or DOCX layouts;
- reference retrieval uses lexical and topic-based scoring rather than production-grade vector search;
- flag generation is rule-based and cannot replace expert legal judgement;
- evaluation is based on a small safe/risky sample set;
- retrieved snippets may not always be the best legal reference;
- the system has not yet been integrated with Azure AI Search or Microsoft Foundry;
- all outputs require human review.

---

## 12. Next Steps

The next stage of work will focus on:

- refining the Streamlit UI for final demonstration;
- preparing final presentation slides;
- preparing a clear demo script;
- improving the written explanation of the system architecture;
- cleaning the repository before the final GitHub upload;
- ensuring internal UoA reference documents are excluded from the public repository;
- optionally exploring Azure AI / Microsoft Foundry integration if time allows.

---

## 13. Summary

At Checkpoint 2, our team has moved beyond ideation and has implemented a working end-to-end MVP.

The system can load contract documents, classify contract type, segment clauses, retrieve reference materials, compare clauses, generate review flags, produce structured reports, and present results through a web interface.

The MVP is ready for demonstration, while still maintaining clear human-in-the-loop boundaries and responsible AI limitations.
