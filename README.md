# NyayaLens AI

An explainable legal-document retrieval prototype that returns the most relevant passages, a transparent urgency signal, and citations for every result. It is intentionally local and deterministic, so reviewers can run and inspect the complete NLP pipeline without an API key.

> Educational portfolio project only. The included corpus is synthetic and the output is not legal advice.

## Why this project

Many chatbot demos hide retrieval quality behind an LLM. NyayaLens makes the evidence layer visible: tokenization, inverse-document-frequency weighting, cosine similarity, and rule-based urgency signals are all small, tested Python components.

## Architecture

```text
question -> tokenizer -> TF-IDF query vector -> cosine ranking -> cited passages
       \-> transparent urgency rules -----------------------> triage label
```

## Try it

```bash
python -m nyayalens.cli "My employer has not paid my final salary"
```

From a fresh clone:

```bash
PYTHONPATH=src python -m nyayalens.cli "My employer has not paid my final salary"
PYTHONPATH=src python -m unittest discover -s tests -v
```

## What recruiters can inspect

- A reusable `TfidfRetriever` with no hidden services or network calls
- Ranked evidence with stable document IDs and relevance scores
- An explainable `UrgencyTriage` component instead of an opaque label
- Unit tests for ranking, empty queries, citations, and triage behavior
- A JSONL corpus format that can be replaced with verified source material

## Production roadmap

- Hybrid BM25 + embedding search with a reranker
- Human-reviewed evaluation set with Recall@k and nDCG
- Versioned source ingestion and citation-level audit logs
- Guardrailed LLM synthesis that is allowed to answer only from retrieved evidence

