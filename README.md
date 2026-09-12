# doc-timeline-synthesizer

[繁體中文](README.zh-TW.md) | English

A provenance-first workflow for turning versioned document collections into
scope-aware, auditable summaries for downstream retrieval and decision support.

The project does not treat the newest value as automatically correct. It first
checks whether candidate values describe the same entity, attribute, period,
scope, unit, and field semantics. Recency is then considered together with
document status, approval state, and provenance. If authority cannot be
resolved, the conflict remains explicit.

## Architecture

The workflow separates three responsibilities:

1. L1 — physical conversion
   - Converts DOCX, PDF, XLSX, PPTX, and related files into source.md records.
   - Preserves manifests and evidence artifacts produced by docling-skill.
2. L2 — scope-aware synthesis
   - Orders records chronologically.
   - Removes repeated administrative boilerplate.
   - Extracts comparable claims and resolves only evidence-supported versions.
   - Produces citation-backed domain summaries.
3. L3 — fresh-context audit
   - Reviews an already-produced summary against the source corpus.
   - Receives neither the producer's conversation history nor reasoning trace.
   - Checks citation resolvability, source risk, cross-version splicing,
     coverage, arithmetic, and statistical scope.
   - Context separation is not the same as model-family independence.
4. Downstream integration — Hierarchical Dual-Store RAG
   - Maintains separate vector/hybrid collections for granular raw documents
     (`source.rag.md`) and audited SSoT reports (`reports/*.md`).
   - Retrieves from both collections simultaneously.
   - Uses priority arbitration prompting: the generator is instructed to treat
     audited SSoT reports as authoritative on disputed facts while citing raw
     provenance for granular situational details.

## Core rules

- Compare scope before comparing dates.
- Treat recency as one authority signal, not a universal overwrite rule.
- Do not assume structured fields always outrank narrative text.
- Record the source, date, section or table, and selection rationale for each
  decision-relevant claim.
- Preserve unresolved conflicts instead of forcing a single answer.
- Never combine units or attributes taken from incompatible versions.
- Inspect unresolved image placeholders before declaring that evidence is
  absent.
- Run a fresh-context audit before treating a high-stakes summary as
  decision-ready.
- In downstream RAG, segregate raw document chunks and audited SSoT summaries
  into dual stores and enforce priority arbitration prompting.

## Installation

Python 3.10 or later and uv are recommended.

    git clone https://github.com/gemini960114/doc-timeline-synthesizer.git
    cd doc-timeline-synthesizer
    uv sync

The L1 conversion stage depends on docling-skill, declared in pyproject.toml.

## Quick start

Use a local directory that is excluded from version control:

    data/
      example_domain/
        2025-01-10_initial_plan.docx
        2025-03-15_approved_revision.pdf

Convert documents with docling-skill, then create a chronological inventory:

    uv run python scripts/synthesize.py       --input-dir output/example_domain       --output-file output/example_domain_inventory.md

Scan for unresolved embedded-image placeholders:

    uv run python scripts/scan_image_placeholders.py       --input-dir output/example_domain

After image evidence has been described or deliberately marked out of scope,
ask an agent using SKILL.md to perform scope-aware synthesis. The synthesis
prompt should require:

- complete reading of every source.md and relevant sidecar;
- comparison by entity, attribute, period, scope, unit, and semantics;
- authority decisions based on provenance and document state;
- citations for every consequential value;
- explicit retention of unresolved conflicts.

Run the L3 review in a fresh agent context using
doc-timeline-auditor/SKILL.md. Finally, build files for RAG ingestion:

    uv run python scripts/build_rag_bundle.py       --input-dir output/example_domain

See EXAMPLE.md for a synthetic end-to-end walkthrough.

## Inputs and generated artifacts

Expected L1 source directory:

    output/example_domain/document_id/
      source.md
      source.manifest.json
      source.evidence.json
      source.images.md
      source.images.skip.json

source.images.md and source.images.skip.json are optional and mutually
purpose-specific. Generated source.rag.md files are disposable and should be
rebuilt whenever their inputs change.

## Empirical quantitative evaluation

The workflow's downstream retrieval impact was evaluated on an adversarial
100-question benchmark featuring temporal superseded revisions, multi-year
trajectory tracking, cross-entity traps, and conflicting legislative proposals:

| Retrieval & Context Architecture | Accuracy | Context Tokens (Prompt) |
|:---|---:|---:|
| Naive Dense Vector RAG (Raw only, Top-5) | 39.0% | ~1,750 tokens |
| Hybrid RAG (BM25 + Dense) + BGE Reranker (Top-5) | 46.0% | ~1,750 tokens |
| Full-Context Baseline (SSoT stuffed into prompt) | **87.0%** | >21,000 tokens |
| **Hierarchical Dual-Store RAG (Raw Top-5 + SSoT Top-5)** | **85.0%** | **~3,500 tokens** |

The Hierarchical Dual-Store design achieves parity with full-context synthesis
(85.0% vs. 87.0%, McNemar's $p = 0.814$) while reducing context window token
overhead by **83.3%** and outperforming standard single-store RAG baselines
statistically significantly ($p < 0.001$).

## Security and data boundary

The public repository contains generic workflow instructions and utilities
only. It does not include the research corpus, internal administrative
documents, raw conversations, derived record-level research ledgers, or
manuscript supplements.

In accordance with institutional data governance and ethical requirements (ISS-06):
- The `evaluation/` directory houses local evaluation scripts and configurations.
- All live API keys (`evaluation/.env`), local virtual environments (`evaluation/.venv/`),
  and binary vector stores (`evaluation/chroma_db/`) are strictly excluded.
- Un-anonymized benchmark question datasets (`evaluation/benchmark/`) and model
  prompt execution traces (`evaluation/results/`) contain proprietary administrative
  case metadata and must remain local and ignored.

Keep source material under ignored local directories. Before every public
push, inspect the staged tree rather than relying only on filename patterns:

    git status --short
    git diff --cached
    git ls-files

Never commit API keys, access tokens, local absolute paths, source documents,
evidence payloads, vector indices, or generated reports.

## Reproducibility boundary

The repository supports inspection and reuse of the generic workflow. It is
not a complete replication package for any study that uses private or
restricted source documents. Results from a particular corpus require
separate authorization and human verification.

## Citation

If you use this codebase or refer to the methodology, please cite:

```bibtex
@article{chuang2026resolving,
  title   = {Resolving Knowledge Conflicts in Versioned Documents with Hierarchical Dual-Store RAG},
  author  = {Chuang, Chao-Chun and Yao, Chih-Min and Lee, Tsui-Mei and Liu, Yi-Ni},
  journal = {arXiv preprint},
  year    = {2026},
  url     = {https://github.com/gemini960114/doc-timeline-synthesizer}
}
```

Machine-readable citation metadata is also maintained in [CITATION.cff](file:///home/ubuntu/github/doc-timeline-synthesizer/CITATION.cff). An updated preprint identifier (arXiv ID and DOI) will be integrated once issued.


## License

MIT. See LICENSE.
