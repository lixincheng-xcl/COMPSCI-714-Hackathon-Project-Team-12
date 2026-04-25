# Evaluation Plan

## 1. Evaluation Goal

The goal of evaluation is to assess whether the proof of concept is useful, explainable, and reliable enough for a classroom demo.

This project does not aim to evaluate legal correctness. The focus is on whether the system can support human review.

## 2. Evaluation Criteria

| Criterion | Description |
|---|---|
| Text extraction quality | Whether contract text is extracted correctly |
| Clause segmentation quality | Whether clauses are split into meaningful units |
| Retrieval relevance | Whether retrieved reference materials are relevant |
| Flag reasonableness | Whether Green / Amber / Red / Blue flags are reasonable |
| Explanation clarity | Whether rationales are understandable |
| Human oversight | Whether outputs clearly require human review |

## 3. Benchmark Plan

A small benchmark set will be created using sample or anonymised contracts.

For each benchmark case, we will record:

- contract type;
- selected clauses;
- expected reference materials;
- expected flag category;
- notes from manual review.

## 4. Limitations

The evaluation is limited by:

- small sample size;
- availability of reference materials;
- variability in contract structures;
- lack of professional legal validation.
