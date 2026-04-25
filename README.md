# 🔥 Hackathon Project: Research Contract Adviser Agent - Team 12

> **COMPSCI 714 - AI Architecture and Design**  
> University of Auckland · Group Project · Semester 1, 2026

[![Course](https://img.shields.io/badge/COMPSCI%20714-AI--Architecture--and--Design-blue)](https://www.auckland.ac.nz/)  
[![Topic](https://img.shields.io/badge/Topic-Research--Contract--Adviser--Agent-purple)](#)  
[![Python](https://img.shields.io/badge/Python-3.9%2F3.11-blue)](https://www.python.org/)  
[![Architecture](https://img.shields.io/badge/Architecture-RAG--based-success)](#)  
[![UI](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)  
[![Version Control](https://img.shields.io/badge/Version%20Control-GitHub-black)](https://github.com/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

<p align="center">
  <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=60" width="820" alt="Banner" />
</p>

---

## 📌 Project Overview

The **Research Contract Adviser Agent** is a proof-of-concept AI system developed by **Team 12 – NovaMind Collective** for the COMPSCI 714 hackathon-based group project.

The project focuses on supporting university staff in reviewing externally drafted research contracts. In a university research context, contracts often need to be checked against internal templates, contracting positions, and institutional requirements. This process can be repetitive, time-consuming, and difficult to perform consistently.

Our system aims to assist human reviewers by analysing uploaded contracts, identifying key clauses, retrieving relevant reference materials, comparing clauses against standard positions, and generating a structured review report.

The system is designed as a **human-in-the-loop decision-support tool**. It does **not** provide legal advice, approve contracts, or replace professional judgement.

---

## 🎯 Selected Use Case

**Use Case:** Research Contract Adviser Agent  
**Team:** Team 12 – NovaMind Collective  
**Course:** COMPSCI 714 – AI Architecture and Design  
**Project Type:** Hackathon-based AI proof of concept

The selected use case focuses on building an AI assistant that can:

- recognise the type of uploaded research contract;
- extract and segment key clauses;
- retrieve relevant university templates and contracting positions;
- compare uploaded clauses against standard references;
- identify deviations, missing coverage, or potential risks;
- generate a structured review report using four flag categories.

---

## 🧠 Problem Understanding

Research contracts often contain complex clauses related to intellectual property, confidentiality, publication rights, liability, data use, termination, payment, and governing law. Manually checking these clauses against institutional standards can be slow and inconsistent.

Our team understands this problem as a **document intelligence and decision-support task**. The key challenge is not simply to generate a summary of a contract, but to build a system that can provide grounded, traceable, and explainable support for contract review.

Therefore, our solution focuses on:

- clause-level analysis rather than only whole-document summarisation;
- retrieval from trusted reference materials;
- structured comparison between uploaded clauses and standard positions;
- explainable flag generation;
- clear human oversight and responsible AI boundaries.

---

## 🚩 Output Categories

The final review report will organise findings into four categories:

| Flag Type | Meaning |
|---|---|
| 🟢 Green Flag | The clause appears aligned with standard university positions. |
| 🟠 Amber Flag | The clause may require further review by a contract manager. |
| 🔴 Red Flag | The clause appears to conflict with standard university positions. |
| 🔵 Blue Flag | The clause or issue is not clearly covered by existing standard references. |

These flags are intended to help human reviewers prioritise attention and make informed decisions.

---

## 🏗️ Proposed System Pipeline

The MVP follows the pipeline below:

```text
Contract Upload
      ↓
Text Extraction
      ↓
Clause Segmentation
      ↓
Contract Type Recognition
      ↓
Reference Retrieval
      ↓
Clause-Level Comparison
      ↓
Flag Generation
      ↓
Structured Review Report
```

### Main Components

| Component | Description |
|---|---|
| Document Ingestion | Reads PDF/DOCX contract files and extracts raw text. |
| Clause Segmentation | Splits contract text into structured clauses. |
| Contract Classification | Identifies the likely type of contract. |
| Reference Retrieval | Retrieves relevant templates or contracting positions. |
| Clause Comparison | Compares uploaded clauses with reference materials. |
| Flag Generation | Assigns Green, Amber, Red, or Blue flags. |
| Report Generation | Produces a structured review report for human review. |

---

## 🧩 MVP Scope

### ✅ In Scope

The first MVP will focus on:

- uploading sample or anonymised contracts;
- extracting text from PDF/DOCX files;
- segmenting contracts into clauses;
- recognising basic contract types;
- retrieving relevant reference clauses;
- performing basic clause-level comparison;
- generating Green / Amber / Red / Blue flags;
- producing a structured review report;
- showing evidence or rationale for generated flags.

### ❌ Out of Scope

The system will not:

- provide legal advice;
- automatically approve or reject contracts;
- integrate with live university contract management systems;
- process confidential real contracts without anonymisation;
- make final decisions on behalf of human reviewers.

---

## 📁 Repository Structure

```text
research-contract-adviser-agent/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── docs/
│   ├── checkpoint1/
│   ├── checkpoint2/
│   ├── project_plan.md
│   ├── architecture.md
│   ├── data_inventory.md
│   ├── risk_register.md
│   └── meeting_notes/
│
├── data/
│   ├── README.md
│   ├── sample_contracts/
│   ├── reference_templates/
│   ├── private/
│   └── processed/
│
├── src/
│   ├── ingest/
│   │   └── document_loader.py
│   ├── preprocess/
│   │   └── clause_segmenter.py
│   ├── classify/
│   │   └── contract_classifier.py
│   ├── retrieve/
│   │   └── retriever.py
│   ├── compare/
│   │   └── clause_comparator.py
│   ├── report/
│   │   └── report_generator.py
│   ├── ui/
│   │   └── app.py
│   └── main.py
│
├── prompts/
│   └── review_prompt.md
│
├── evaluation/
│   ├── benchmark_cases.md
│   └── evaluation_plan.md
│
├── tests/
│   └── test_pipeline.py
│
└── outputs/
    └── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd research-contract-adviser-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

Do not commit `.env` to GitHub.

---

## ▶️ How to Run

### Run the Basic Pipeline

```bash
python src/main.py
```

### Run the Demo UI

```bash
streamlit run src/ui/app.py
```

The demo UI will allow users to upload a sample contract and view the generated review report.

---

## 👥 Team Roles

| Member | Role | Main Responsibility |
|---|---|---|
| Andrew Horse | Project Lead | Project coordination, timeline management, submissions, final presentation structure |
| Ocean Cao | Data & Problem Analyst | Problem analysis, data inventory, clause taxonomy, evaluation design |
| Craig Newkirk | Solution Architect | System architecture, technical design, module interface planning |
| Xincheng Li | Implementation Lead | PoC implementation, code integration, GitHub management, demo setup |
| Jeff Dong | AI Governance Lead | Responsible AI, privacy, risk analysis, governance documentation |

---

## 🗓️ Development Roadmap

### Week 1: Repository Setup and Use Case Understanding

- Set up GitHub repository.
- Create README, folder structure, and documentation files.
- Review use case requirements.
- Prepare initial project plan.

### Week 2: Problem and Data Analysis

- Define problem scope.
- Create clause taxonomy.
- Prepare data inventory.
- Identify sample contracts and reference materials.

### Week 3: Architecture and Document Processing

- Finalise system architecture.
- Implement document loading.
- Extract text from PDF/DOCX files.
- Create initial clause segmentation logic.

### Week 4: Retrieval and Clause Matching

- Build reference template index.
- Implement basic retrieval.
- Match uploaded clauses with reference clauses.
- Prepare Checkpoint 2 materials.

### Week 5: Clause Comparison and Flag Generation

- Implement comparison logic.
- Generate Green / Amber / Red / Blue flags.
- Add evidence and rationale for each flag.

### Week 6: Report Generation and UI

- Generate structured review reports.
- Build Streamlit demo interface.
- Test with sample contracts.
- Improve output readability.

### Week 7: Evaluation and Demo Preparation

- Evaluate system outputs.
- Conduct error analysis.
- Refine responsible AI safeguards.
- Prepare final demo and presentation materials.

---

## ✅ Current Development Status

| Module | Status |
|---|---|
| GitHub repository setup | In Progress |
| README documentation | In Progress |
| Project structure | Not Started |
| Document ingestion | Not Started |
| Clause segmentation | Not Started |
| Contract type recognition | Not Started |
| Reference retrieval | Not Started |
| Clause comparison | Not Started |
| Flag generation | Not Started |
| Report generation | Not Started |
| Demo UI | Not Started |
| Evaluation | Not Started |
| Responsible AI review | In Progress |

---

## 🧪 Evaluation Plan

The MVP will be evaluated using a small benchmark set of sample or anonymised contracts.

Potential evaluation criteria include:

- whether the system correctly extracts contract text;
- whether clauses are segmented accurately;
- whether relevant reference materials are retrieved;
- whether generated flags are reasonable;
- whether explanations are clear and useful;
- whether the report supports human review without making final legal decisions.

The evaluation will focus on usefulness, explainability, and reliability rather than full legal correctness.

---

## 🛡️ Responsible AI and Governance

Because contract documents may contain confidential or commercially sensitive information, the project must follow responsible AI principles.

Key governance principles:

- Use anonymised or sample contracts only.
- Do not upload confidential contracts to public repositories.
- Do not commit API keys or private credentials.
- Provide rationale or evidence for generated flags.
- Keep humans responsible for all final review decisions.
- Clearly state that the system does not provide legal advice.
- Avoid unsupported or overconfident outputs.
- Maintain transparency in how results are generated.

---

## 🔐 Data and Privacy Notice

Do not upload any real, confidential, or non-anonymised contract documents to this repository.

The following folders should not contain sensitive data:

```text
data/private/
data/raw/
data/processed/
```

Any real contract data must be anonymised before use. Sensitive files should be stored securely outside the public GitHub repository.

---

## 🌱 Branching and Contribution Workflow

### Branch Naming

Use descriptive branch names:

```text
feature/document-ingestion
feature/clause-segmentation
feature/reference-retrieval
feature/report-generation
docs/checkpoint2
docs/architecture
fix/ui-bug
```

### Commit Message Examples

```bash
git commit -m "feat: add PDF text extraction module"
git commit -m "feat: implement basic clause segmentation"
git commit -m "docs: add system architecture draft"
git commit -m "fix: handle empty document upload"
```

### Pull Request Rules

Before merging into `main`:

1. Create a pull request.
2. Request review from at least one teammate.
3. Ensure the code runs locally.
4. Do not include sensitive data or API keys.
5. Update documentation if the change affects usage.

---

## 📌 Project Management

We use GitHub Issues and Project Board to track work.

Suggested issue labels:

```text
documentation
implementation
architecture
data
evaluation
governance
bug
enhancement
checkpoint-2
demo
high-priority
```

Suggested board columns:

```text
Backlog
To Do
In Progress
Review
Done
Blocked
```

---

## 📄 Coursework Deliverables

| Deliverable | Description | Status |
|---|---|---|
| Team Registration | Confirm team members and roles | Completed |
| Use Case Selection | Select Research Contract Adviser Agent | Completed |
| Checkpoint 1 | Problem understanding, ideation, initial design | Completed |
| Checkpoint 2 | Solution architecture and implementation progress | Pending |
| Final Presentation | Pitch and demo of PoC | Pending |
| Final Report | Technical report and reflection | Pending |

---

## ⚠️ Disclaimer

This project is developed for academic coursework purposes only.

The system is an experimental proof of concept. It is not a legal tool and must not be used as a substitute for professional contract review or legal advice.

---

## 📜 License

This project is licensed under the MIT License.
