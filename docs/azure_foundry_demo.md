# Azure / Microsoft Foundry Demo Notes

## 1. Azure Component Overview

This project includes an Azure / Microsoft Foundry demonstration component.

A Microsoft Foundry Agent has been created for the project:

- Agent name: Research-Contract-Adviser-Agent-Team-12
- Model deployment: gpt-4o
- Purpose: clause-level contract review explanation support

The Azure Agent demonstrates the explanation layer of the Research Contract Adviser Agent. It supports human reviewers by explaining clause-level review results in professional language.

---

## 2. Relationship Between Azure Agent and Local Pipeline

The project contains two complementary parts.

### Local Python / Streamlit Pipeline

The local pipeline performs the deterministic review workflow:

Document loading  
→ Contract type recognition  
→ Clause segmentation  
→ Reference retrieval  
→ Clause comparison  
→ Green / Amber / Red / Blue flag generation  
→ Markdown / JSON report generation  
→ Streamlit UI display

The local pipeline is responsible for flag assignment and structured reporting.

### Microsoft Foundry Agent

The Microsoft Foundry Agent uses the gpt-4o deployment to explain review results.

The Azure Agent does not assign or change Green / Amber / Red / Blue flags. It is used to demonstrate how Azure can support explanation, communication, and human review.

---

## 3. Responsible AI Design

The system follows a human-in-the-loop design.

The system does not:

- provide legal advice;
- approve or reject contracts;
- replace contract managers or legal professionals;
- make final legal conclusions.

The deterministic local pipeline controls the review workflow and flag generation. Azure is used as an explanation support layer, not as an autonomous legal decision-maker.

---

## 4. Demo Strategy

The final demo should be presented in two parts.

### Part A: Microsoft Foundry Agent Demo

Open Microsoft Foundry and show:

- the team-12 project;
- the Research-Contract-Adviser-Agent-Team-12 Agent;
- the gpt-4o model deployment;
- the Agent instructions;
- the Playground response to a risky confidentiality clause.

Example prompt:

A confidentiality clause says the University must keep all confidential information secret forever and without exception. The local system assigned a Red flag. Explain why this requires human review.

Expected behaviour:

The Agent should explain why the clause requires human review, while avoiding legal advice and avoiding final approval or rejection.

### Part B: Streamlit System Demo

Run the local Streamlit application:

streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501

Then demonstrate:

Safe sample contract:

- Red: 0
- Amber: 2
- Blue: 0
- Green: 5

Risky sample contract:

- Red: 6
- Amber: 1
- Blue: 0
- Green: 0

This demonstrates the full contract review workflow.

---

## 5. Why Live Azure Calls Are Disabled in AutoDL

Live Azure calls are disabled by default in the AutoDL runtime:

AZURE_EXPLANATIONS_ENABLED=false

This is because external network latency or DNS resolution from AutoDL to Azure may affect demo reliability.

The Azure integration has been tested successfully, and the Microsoft Foundry Agent can be demonstrated directly in the Azure portal. The Streamlit app remains stable and deterministic for the main contract review demo.

---

## 6. Final Explanation for Presentation

Our system uses Azure in two ways.

First, we created a Microsoft Foundry Agent using the gpt-4o deployment to demonstrate Azure-based explanation support.

Second, our Python project includes an Azure explanation enhancement module. This module is designed to improve clause-level rationales without changing the review flags.

The local pipeline remains responsible for document processing, clause segmentation, reference retrieval, clause comparison, and Green / Amber / Red / Blue flag assignment. This design keeps the system explainable, controlled, and human-in-the-loop.
