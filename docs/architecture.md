# System Architecture

## 1. Overview

The Research Contract Adviser Agent is designed as a human-in-the-loop AI system for supporting university research contract review.

The system follows a retrieval-augmented and rule-guided architecture rather than a purely generative chatbot. The purpose is to provide grounded, explainable, and traceable support for contract reviewers.

## 2. High-Level Pipeline

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

## 3. Main Modules

| Module | Purpose |
|---|---|
| Document Ingestion | Load PDF/DOCX files and extract text |
| Clause Segmentation | Split contract text into structured clauses |
| Contract Classification | Identify likely contract type |
| Reference Retrieval | Retrieve relevant templates and contracting positions |
| Clause Comparison | Compare uploaded clauses with standard references |
| Flag Generation | Assign Green / Amber / Red / Blue flags |
| Report Generation | Generate structured review report |
| Demo UI | Allow users to upload contracts and view results |

## 4. Design Rationale

The system uses retrieval and clause-level comparison because contract review requires grounded reasoning against trusted references. The system should not freely generate legal conclusions.

## 5. Human-in-the-Loop Design

The system is intended to assist reviewers only. It does not provide legal advice, approve contracts, or make final decisions.

Each generated flag should include:

- the uploaded clause;
- the retrieved reference clause or policy position;
- the assigned flag;
- a short rationale;
- a reminder that human review is required.
