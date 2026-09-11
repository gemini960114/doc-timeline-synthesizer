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

## Security and data boundary

The public repository contains generic workflow instructions and utilities
only. It does not include the research corpus, internal administrative
documents, raw conversations, derived record-level research ledgers, or
manuscript supplements.

Keep source material under ignored local directories. Before every public
push, inspect the staged tree rather than relying only on filename patterns:

    git status --short
    git diff --cached
    git ls-files

Never commit API keys, access tokens, local absolute paths, source documents,
evidence payloads, or generated reports.

## Reproducibility boundary

The repository supports inspection and reuse of the generic workflow. It is
not a complete replication package for any study that uses private or
restricted source documents. Results from a particular corpus require
separate authorization and human verification.

## Citation

Citation metadata for the software is provided in CITATION.cff. An associated
preprint citation can be added after an arXiv identifier is assigned.

## License

MIT. See LICENSE.
