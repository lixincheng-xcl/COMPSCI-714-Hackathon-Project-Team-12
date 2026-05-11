# 🔥 Hackathon Project: Research Contract Adviser Agent - Team 12

> **COMPSCI 714 - AI Architecture and Design**  
> University of Auckland · Group Project · Semester 1, 2026

[![Course](https://img.shields.io/badge/COMPSCI%20714-AI--Architecture--and--Design-blue)](https://www.auckland.ac.nz/)  
[![Topic](https://img.shields.io/badge/Topic-Research--Contract--Adviser--Agent-purple)](#)  
[![Python](https://img.shields.io/badge/Python-3.9%2F3.12-blue)](https://www.python.org/)  
[![Architecture](https://img.shields.io/badge/Architecture-RAG--based-success)](#)  
[![UI](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)  
[![Azure](https://img.shields.io/badge/Azure-Microsoft%20Foundry-blue)](https://ai.azure.com/)  
[![Model](https://img.shields.io/badge/Model-gpt--4o-purple)](#)  
[![Version Control](https://img.shields.io/badge/Version%20Control-GitHub-black)](https://github.com/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

<p align="center">
  <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=60" width="820" alt="Banner" />
</p>

---

## 📌 Project Overview

The **Research Contract Adviser Agent** is a proof-of-concept AI system developed by **Team 12 – NovaMind Collective** for the COMPSCI 714 hackathon-based group project.

The project supports university staff in reviewing externally drafted research contracts. In a university research context, contracts often need to be checked against internal templates, contracting positions, and institutional requirements. This process can be repetitive, time-consuming, and difficult to perform consistently.

Our system assists human reviewers by:

- loading contract documents;
- identifying the likely contract type;
- segmenting contracts into clauses;
- retrieving relevant university reference materials;
- comparing uploaded clauses against standard positions;
- generating Green / Amber / Red / Blue review flags;
- producing structured Markdown and JSON review reports;
- demonstrating Azure / Microsoft Foundry explanation support.

The system is designed as a **human-in-the-loop decision-support tool**. It does **not** provide legal advice, approve contracts, reject contracts, or replace professional judgement.

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
- generate a structured review report using four flag categories;
- support human review through responsible AI and Azure-based explanation support.

---

## ✅ Current MVP Status

The project has reached a demonstrable MVP stage.

The current system supports:

- TXT, PDF, and DOCX contract loading;
- contract type recognition;
- clause segmentation;
- UoA reference template and contracting position loading;
- reference retrieval;
- clause-level comparison;
- Green / Amber / Red / Blue flag generation;
- Markdown and JSON report generation;
- Streamlit web demo;
- Microsoft Foundry Agent demonstration;
- Azure OpenAI explanation enhancement module;
- automated pipeline tests.

The current stable AutoDL runtime uses the deterministic local review pipeline for the Streamlit demo. Azure / Microsoft Foundry is demonstrated separately through the Microsoft Foundry Agent because live Azure calls from AutoDL may be affected by external network latency.

---

## 🧠 Problem Understanding

Research contracts often contain complex clauses related to intellectual property, confidentiality, publication rights, liability, data use, termination, payment, and governing law. Manually checking these clauses against institutional standards can be slow and inconsistent.

Our team understands this problem as a **document intelligence and decision-support task**. The key challenge is not simply to generate a summary of a contract, but to build a system that can provide grounded, traceable, and explainable support for contract review.

Therefore, our solution focuses on:

- clause-level analysis rather than only whole-document summarisation;
- retrieval from trusted reference materials;
- structured comparison between uploaded clauses and standard positions;
- explainable flag generation;
- clear human oversight and responsible AI boundaries;
- Azure / Microsoft Foundry support for explanation and human-review communication.

---

## 🚩 Output Categories

The final review report organises findings into four categories:

| Flag Type | Meaning |
|---|---|
| 🟢 Green Flag | The clause appears aligned with standard university positions. |
| 🟠 Amber Flag | The clause may require further review by a contract manager. |
| 🔴 Red Flag | The clause appears to conflict with standard university positions or contains high-risk wording. |
| 🔵 Blue Flag | The clause or issue is not clearly covered by existing standard references. |

These flags help human reviewers prioritise attention and make informed decisions.

---

## 🏗️ System Pipeline

The current MVP follows the pipeline below:

```text
Document input
      ↓
Text extraction
      ↓
Contract type recognition
      ↓
Clause segmentation
      ↓
Reference document loading
      ↓
Reference retrieval
      ↓
Clause-level comparison
      ↓
Green / Amber / Red / Blue flag generation
      ↓
Markdown / JSON report generation
      ↓
Streamlit demo UI
```

### Main Components

| Component | Description | Status |
|---|---|---|
| Document Loader | Reads TXT, PDF, and DOCX files and extracts plain text. | Completed |
| Clause Segmenter | Splits extracted contract text into structured clause objects. | Completed |
| Contract Classifier | Identifies the likely type of contract. | Completed |
| Reference Loader | Loads local UoA templates and contracting positions. | Completed |
| Reference Retriever | Retrieves relevant reference chunks for each clause. | Completed |
| Clause Comparator | Compares uploaded clauses with retrieved reference material. | Completed |
| Flag Generator | Assigns Green, Amber, Red, or Blue flags. | Completed |
| Report Generator | Produces Markdown and JSON reports. | Completed |
| Streamlit UI | Provides a web-based demo interface. | Completed |
| Azure Explainer | Uses Azure OpenAI / Microsoft Foundry for explanation enhancement. | Implemented |
| Microsoft Foundry Agent | Demonstrates Azure-based agent explanation support. | Completed |
| Automated Tests | Validates the main pipeline. | Completed |

---

## 🤖 Azure / Microsoft Foundry Agent Demo

The project includes an Azure / Microsoft Foundry demonstration component.

A Microsoft Foundry Agent has been created for the project:

- **Agent name:** Research-Contract-Adviser-Agent-Team-12
- **Model deployment:** gpt-4o
- **Purpose:** clause-level contract review explanation support

The Azure Agent demonstrates the explanation layer of the Research Contract Adviser Agent. It supports human reviewers by explaining clause-level review results in professional language.

The Azure Agent does **not** assign or change Green / Amber / Red / Blue flags. The deterministic Python pipeline remains responsible for document loading, clause segmentation, reference retrieval, clause comparison, and flag generation.

For reliability during the AutoDL-based Streamlit demo, live Azure calls are disabled by default:

```env
AZURE_EXPLANATIONS_ENABLED=false
```

This avoids external network latency affecting the main contract review demo. The Azure Agent can be demonstrated directly in Microsoft Foundry Playground.

For details on how Azure is used in the final demonstration, see:

```text
docs/azure_foundry_demo.md
```

---

## 🧩 MVP Scope

### ✅ In Scope

The MVP currently supports:

- loading safe sample or anonymised contracts;
- extracting text from TXT, PDF, and DOCX files;
- segmenting contracts into clauses;
- recognising basic contract types;
- retrieving relevant reference clauses;
- performing clause-level comparison;
- generating Green / Amber / Red / Blue flags;
- producing Markdown and JSON review reports;
- displaying results in Streamlit;
- demonstrating Azure / Microsoft Foundry explanation support;
- showing evidence and rationale for generated flags.

### ❌ Out of Scope

The system does not:

- provide legal advice;
- automatically approve or reject contracts;
- replace contract managers or legal professionals;
- process confidential real contracts without anonymisation;
- make final decisions on behalf of human reviewers;
- deploy the full Streamlit web application to Azure App Service in the current MVP.

---

## 📁 Repository Structure

```text
COMPSCI-714-Hackathon-Project-Team-12/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── docs/
│   ├── checkpoint1/
│   ├── checkpoint2/
│   ├── azure_foundry_demo.md
│   ├── demo_script.md
│   ├── implementation_progress.md
│   ├── project_plan.md
│   ├── architecture.md
│   ├── data_inventory.md
│   ├── risk_register.md
│   └── meeting_notes/
│
├── data/
│   ├── README.md
│   ├── sample_contracts/
│   │   ├── sample_contract.txt
│   │   └── risky_contract.txt
│   ├── reference_templates/
│   ├── reference_positions/
│   ├── private/
│   └── processed/
│
├── src/
│   ├── azure/
│   │   ├── __init__.py
│   │   ├── azure_explainer.py
│   │   ├── azure_sanity_check.py
│   │   ├── test_azure_explainer.py
│   │   └── test_pipeline_with_azure.py
│   │
│   ├── classify/
│   │   └── contract_classifier.py
│   │
│   ├── compare/
│   │   └── clause_comparator.py
│   │
│   ├── ingest/
│   │   └── document_loader.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── review_pipeline.py
│   │
│   ├── preprocess/
│   │   └── clause_segmenter.py
│   │
│   ├── report/
│   │   └── report_generator.py
│   │
│   ├── retrieve/
│   │   ├── reference_loader.py
│   │   └── retriever.py
│   │
│   ├── ui/
│   │   └── app.py
│   │
│   ├── run_review.py
│   ├── generate_report.py
│   ├── inspect_references.py
│   └── test_retrieval.py
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
    ├── sample_contract_review_report.md
    ├── sample_contract_review_report.json
    ├── risky_contract_review_report.md
    └── risky_contract_review_report.json
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd COMPSCI-714-Hackathon-Project-Team-12
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

Example `.env`:

```env
AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
AZURE_OPENAI_BASE_URL=https://ai-team-12-hack.services.ai.azure.com/openai/v1/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_EXPLANATIONS_ENABLED=false
```

---

## ▶️ Main Entry Points

| Purpose | Command |
|---|---|
| Run Streamlit demo UI | `streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501` |
| Run safe sample review | `python src/run_review.py data/sample_contracts/sample_contract.txt` |
| Run risky sample review | `python src/run_review.py data/sample_contracts/risky_contract.txt` |
| Generate reports | `python src/generate_report.py data/sample_contracts/sample_contract.txt` |
| Inspect reference documents | `python src/inspect_references.py` |
| Test retrieval quality | `python src/test_retrieval.py data/sample_contracts/sample_contract.txt` |
| Test Azure connection | `python src/azure/azure_sanity_check.py` |
| Test Azure explainer | `python src/azure/test_azure_explainer.py` |
| Run automated tests | `pytest -q` |

---

## 🚀 Quick Start

### 1. Activate Environment

```bash
cd /root/autodl-tmp/COMPSCI-714-Hackathon-Project-Team-12
source .venv/bin/activate
```

### 2. Run Automated Tests

```bash
pytest -q
```

Expected output:

```text
8 passed
```

### 3. Run Command-Line Review Pipeline

Safe sample:

```bash
python src/run_review.py data/sample_contracts/sample_contract.txt
```

Expected flag counts:

```text
Green: 5
Amber: 2
Red: 0
Blue: 0
```

Risky sample:

```bash
python src/run_review.py data/sample_contracts/risky_contract.txt
```

Expected flag counts:

```text
Green: 0
Amber: 1
Red: 6
Blue: 0
```

### 4. Run Streamlit Demo

```bash
streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

Then open the browser at:

```text
http://localhost:8501
```

or use the external URL displayed in the terminal when running on AutoDL.

---

## 🧪 Demo Scenarios

### Scenario A: Safe Sample Contract

Input:

```text
data/sample_contracts/sample_contract.txt
```

Expected result:

| Flag | Count |
|---|---:|
| Green | 5 |
| Amber | 2 |
| Red | 0 |
| Blue | 0 |

This demonstrates that the system can identify generally acceptable clauses and classify most of them as Green while keeping uncertain clauses as Amber for human review.

### Scenario B: Risky Sample Contract

Input:

```text
data/sample_contracts/risky_contract.txt
```

Expected result:

| Flag | Count |
|---|---:|
| Green | 0 |
| Amber | 1 |
| Red | 6 |
| Blue | 0 |

The risky sample contains deliberately high-risk clauses related to:

- confidentiality obligations lasting forever;
- assignment of all intellectual property to the external partner;
- publication restrictions;
- unlimited liability;
- termination restrictions;
- non-New Zealand governing law.

This demonstrates that the system can detect high-risk wording and generate Red Flags for human review.

### Scenario C: Microsoft Foundry Agent Demo

Open Microsoft Foundry and show:

- team-12 project;
- Research-Contract-Adviser-Agent-Team-12 Agent;
- gpt-4o model deployment;
- Agent instructions;
- Playground response to a risky confidentiality clause.

Example prompt:

```text
A confidentiality clause says the University must keep all confidential information secret forever and without exception. The local system assigned a Red flag. Explain why this requires human review.
```

Expected behaviour:

The Agent should explain why the clause requires human review, while avoiding legal advice and avoiding final approval or rejection.

---

## 📊 Testing Results

The current automated test suite passes successfully:

```text
8 passed
```

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
- Extract text from TXT, PDF, and DOCX files.
- Create initial clause segmentation logic.

### Week 4: Retrieval and Clause Matching

- Build reference template index.
- Implement reference retrieval.
- Match uploaded clauses with reference clauses.
- Prepare Checkpoint 2 materials.

### Week 5: Clause Comparison and Flag Generation

- Implement comparison logic.
- Generate Green / Amber / Red / Blue flags.
- Add evidence and rationale for each flag.

### Week 6: Report Generation, UI, and Azure Integration

- Generate structured Markdown and JSON reports.
- Build Streamlit demo interface.
- Connect Azure / Microsoft Foundry gpt-4o deployment.
- Create Azure explanation enhancement module.
- Create Microsoft Foundry Agent.

### Week 7: Evaluation and Demo Preparation

- Evaluate system outputs.
- Conduct error analysis.
- Refine responsible AI safeguards.
- Prepare final demo and presentation materials.
- Clean repository before final GitHub upload.

---

## ✅ Current Development Status

| Module | Status |
|---|---|
| GitHub repository setup | Completed |
| README documentation | Completed |
| Project structure | Completed |
| Document ingestion | Completed |
| Clause segmentation | Completed |
| Contract type recognition | Completed |
| Reference loading | Completed |
| Reference retrieval | Completed |
| Clause comparison | Completed |
| Flag generation | Completed |
| Report generation | Completed |
| Streamlit demo UI | Completed |
| Safe sample demo | Completed |
| Risky sample demo | Completed |
| Automated tests | Completed |
| Azure OpenAI sanity check | Completed |
| Azure explanation enhancement module | Implemented |
| Microsoft Foundry Agent | Completed |
| Azure-aware Streamlit notice | Completed |
| Responsible AI documentation | Completed |
| Final presentation | Pending |
| Final report | Pending |
| Final GitHub cleanup and upload | Pending |

---

## 🧪 Evaluation Plan

The MVP is evaluated using a small benchmark set of safe and risky sample contracts.

Evaluation criteria include:

- whether the system correctly extracts contract text;
- whether clauses are segmented accurately;
- whether the contract type is correctly recognised;
- whether relevant reference materials are retrieved;
- whether generated flags are reasonable;
- whether explanations are clear and useful;
- whether reports support human review without making final legal decisions;
- whether the Streamlit demo can consistently reproduce expected results.

The current benchmark results are:

| Sample | Red | Amber | Blue | Green |
|---|---:|---:|---:|---:|
| Safe sample contract | 0 | 2 | 0 | 5 |
| Risky sample contract | 6 | 1 | 0 | 0 |

---

## 🛡️ Responsible AI and Governance

Because contract documents may contain confidential or commercially sensitive information, the project follows responsible AI principles.

Key governance principles:

- Use anonymised or sample contracts only.
- Do not upload confidential contracts to public repositories.
- Do not commit API keys or private credentials.
- Provide rationale or evidence for generated flags.
- Keep humans responsible for all final review decisions.
- Clearly state that the system does not provide legal advice.
- Avoid unsupported or overconfident outputs.
- Maintain transparency in how results are generated.
- Use Azure / Microsoft Foundry as an explanation support layer rather than an autonomous legal decision-maker.

---

## 🔐 Data and Privacy Notice

Do not upload any real, confidential, or non-anonymised contract documents to this repository.

The following folders may contain internal or sensitive materials and should not be pushed to the public GitHub repository:

```text
data/private/
data/reference_templates/
data/reference_positions/
docs/use_case/
.env
```

The public repository should only include:

- source code;
- safe sample contracts;
- tests;
- generated non-sensitive example outputs;
- documentation.

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
feature/azure-foundry-agent
docs/checkpoint2
docs/architecture
fix/ui-bug
```

### Commit Message Examples

```bash
git commit -m "feat: add PDF text extraction module"
git commit -m "feat: implement basic clause segmentation"
git commit -m "feat: add Azure explanation enhancer"
git commit -m "docs: add Microsoft Foundry demo notes"
git commit -m "fix: handle empty document upload"
```

### Pull Request Rules

Before merging into `main`:

1. Create a pull request.
2. Request review from at least one teammate.
3. Ensure the code runs locally.
4. Do not include sensitive data or API keys.
5. Do not include internal UoA reference files in the public repository.
6. Update documentation if the change affects usage.

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
azure
foundry
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
| Checkpoint 2 | Solution architecture and implementation progress | Completed |
| MVP Implementation | Working local pipeline and Streamlit demo | Completed |
| Azure / Microsoft Foundry Demo | Foundry Agent using gpt-4o | Completed |
| Final Presentation | Pitch and demo of PoC | Pending |
| Final Report | Technical report and reflection | Pending |
| Final GitHub Cleanup | Remove sensitive/internal files before upload | Pending |

---

## ⚠️ Disclaimer

This project is developed for academic coursework purposes only.

The system is an experimental proof of concept. It is not a legal tool and must not be used as a substitute for professional contract review or legal advice.

All outputs require human review.

---

## 📜 License

This project is licensed under the MIT License.
