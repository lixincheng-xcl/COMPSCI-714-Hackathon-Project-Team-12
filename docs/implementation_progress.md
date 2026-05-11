# Implementation Progress - Research Contract Adviser Agent

## 1. Current MVP Status

The Research Contract Adviser Agent has reached a demonstrable MVP stage.

The current system can process a contract document, classify its contract type, segment it into clauses, retrieve relevant UoA reference material, compare clauses against references, generate Green / Amber / Red / Blue review flags, and present the results through a Streamlit web interface.

Current pipeline:

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

---

## 2. Implemented Modules

| Module | File | Status |
|---|---|---|
| Document Loader | src/ingest/document_loader.py | Completed |
| Clause Segmenter | src/preprocess/clause_segmenter.py | Completed |
| Contract Classifier | src/classify/contract_classifier.py | Completed |
| Reference Loader | src/retrieve/reference_loader.py | Completed |
| Reference Retriever | src/retrieve/retriever.py | Completed |
| Clause Comparator and Flag Generator | src/compare/clause_comparator.py | Completed |
| Report Generator | src/report/report_generator.py | Completed |
| Streamlit UI | src/ui/app.py | Completed |
| Pipeline Tests | tests/test_pipeline.py | Completed |

---

## 3. Reference Data Used

The MVP uses UoA reference materials provided through the course project package.

Local reference folders:

- data/reference_templates/
- data/reference_positions/
- docs/use_case/

The reference knowledge base currently includes:

- UoA contract templates;
- UoA Contracting Positions and Approvals / Escalation Protocol;
- Research Contract Adviser Agent use case brief.

These files are stored locally for development and demonstration. They should not be pushed to the public GitHub repository.

---

## 4. Testing Results

The automated test suite has passed successfully:

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

---

## 5. Demo Results

### Safe Sample Contract

Input file:

data/sample_contracts/sample_contract.txt

Expected output:

| Flag | Count |
|---|---:|
| Red | 0 |
| Amber | 2 |
| Blue | 0 |
| Green | 5 |

This demonstrates that the system can identify generally acceptable clauses and classify them mostly as Green, while keeping uncertain clauses as Amber for human review.

### Risky Sample Contract

Input file:

data/sample_contracts/risky_contract.txt

Expected output:

| Flag | Count |
|---|---:|
| Red | 6 |
| Amber | 1 |
| Blue | 0 |
| Green | 0 |

This demonstrates that the system can detect high-risk clauses related to confidentiality, intellectual property assignment, publication restrictions, unlimited liability, termination restrictions, and non-New Zealand governing law.

---

## 6. Responsible AI and Human Oversight

The system is designed as a human-in-the-loop review support tool.

The system does not:

- provide legal advice;
- approve or reject contracts;
- replace contract managers or legal professionals;
- make final legal conclusions.

Each generated result includes:

- clause text;
- retrieved reference source;
- review flag;
- rationale;
- human review requirement.

---

## 7. Current Limitations

The current MVP is functional but has several limitations:

- clause segmentation is rule-based and may not work perfectly for all complex PDF or DOCX layouts;
- reference retrieval uses lexical and topic-based scoring rather than production-grade vector search;
- flag generation is rule-based and cannot replace expert legal judgement;
- evaluation is based on a small safe/risky sample set;
- retrieved snippets may not always be the best possible legal reference;
- all outputs require human review.

---

## 8. Future Improvements

Future work could include:

- integrating Azure AI Document Intelligence for robust document parsing;
- using Azure AI Search or vector retrieval for stronger reference matching;
- using Microsoft Foundry / Azure OpenAI for grounded explanation generation;
- expanding the benchmark set with anonymised contracts;
- improving clause segmentation for complex real-world contracts;
- adding reviewer feedback, audit trails, and exportable review history;
- implementing role-based access and secure document handling.

---

## 9. Current Completion Summary

The current MVP is ready for demonstration.

Completed:

- end-to-end local pipeline;
- Streamlit user interface;
- safe sample demo;
- risky sample demo;
- automated tests;
- downloadable Markdown and JSON reports;
- demo script documentation.

Remaining project work:

- prepare Checkpoint 2 report;
- prepare final presentation slides;
- record or rehearse demo;
- clean repository before final GitHub update;
- ensure internal UoA reference files are excluded from GitHub.
