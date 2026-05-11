# Demo Script - Research Contract Adviser Agent

## 1. Demo Goal

This demo presents a proof-of-concept Research Contract Adviser Agent for supporting university staff in reviewing externally drafted research contracts.

The system can:

- load TXT, PDF, and DOCX contract documents;
- identify the likely contract type;
- segment the contract into clauses;
- retrieve relevant UoA reference templates and contracting positions;
- compare clauses against retrieved references;
- assign Green, Amber, Red, or Blue review flags;
- generate downloadable Markdown and JSON review reports.

The system is designed as a human-in-the-loop review support tool. It does not provide legal advice, approve contracts, or replace professional judgement.

---

## 2. How to Start the Demo

Run the Streamlit app:

streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501

Then open the browser at:

http://localhost:8501

or use the AutoDL external URL shown in the terminal.

---

## 3. Demo Scenario A - Safe Sample Contract

### Step

In the sidebar, select:

Use safe sample contract

Then click:

Run Contract Review

### Expected Result

The system should show:

File: sample_contract.txt  
Contract Type: Research Collaboration Agreement  
Confidence: 1.00  
Clauses: 7

Flag counts:

Red: 0  
Amber: 2  
Blue: 0  
Green: 5

### Explanation

This sample contract contains generally acceptable clauses. Most clauses are classified as Green because they appear aligned with retrieved UoA reference materials. Some clauses are classified as Amber because the system found relevant references but still requires human review.

---

## 4. Demo Scenario B - Risky Sample Contract

### Step

In the sidebar, select:

Use risky sample contract

Then click:

Run Contract Review

### Expected Result

The system should show:

File: risky_contract.txt  
Contract Type: Research Collaboration Agreement  
Confidence: 1.00  
Clauses: 7

Flag counts:

Red: 6  
Amber: 1  
Blue: 0  
Green: 0

### Explanation

This contract deliberately contains high-risk wording. The system detects risks such as:

- confidentiality obligations lasting forever;
- assignment of all intellectual property to the external partner;
- restriction on publication without prior approval;
- unlimited liability;
- no right for the University to terminate;
- non-New Zealand governing law.

These clauses are flagged as Red because they may conflict with standard university positions and require human review.

---

## 5. Demo Scenario C - Upload a Contract

### Step

In the sidebar, select:

Upload a contract

Upload a safe TXT, PDF, or DOCX contract file.

Then click:

Run Contract Review

### Expected Result

The system should:

- read the uploaded file;
- identify the contract type;
- segment clauses;
- retrieve relevant UoA references;
- generate Green, Amber, Red, and Blue flags;
- allow downloading Markdown and JSON reports.

### Important Note

Do not upload confidential or non-anonymised real contracts during the demo.

---

## 6. Key Talking Points

### Problem

University research contracts are often reviewed manually against standard templates and contracting positions. This process can be repetitive, time-consuming, and inconsistent.

### Solution

Our system provides a modular AI-assisted workflow:

Document ingestion  
→ Contract type recognition  
→ Clause segmentation  
→ Reference retrieval  
→ Clause comparison  
→ Flag generation  
→ Structured reporting

### Design Rationale

The system uses a retrieval-augmented and rule-guided design rather than a free-form chatbot. Contract review requires grounded and traceable comparison against trusted reference materials.

### Human Oversight

Each output includes:

- clause text;
- retrieved reference;
- review flag;
- rationale;
- human review requirement.

The system does not provide legal advice or final contract approval.

---

## 7. Current MVP Limitations

The current MVP has several limitations:

- clause segmentation is rule-based and may not work perfectly for all complex contracts;
- reference retrieval uses lexical and topic-based scoring rather than production-grade vector search;
- flag generation is rule-based and cannot replace expert judgement;
- the benchmark set is small;
- all results require human review.

---

## 8. Future Improvements

Future improvements include:

- integrating Azure AI Document Intelligence for stronger document parsing;
- using Azure AI Search or vector retrieval for better reference matching;
- adding LLM-assisted explanations with strict grounding;
- expanding benchmark cases using anonymised contracts;
- adding reviewer feedback and audit trails.
