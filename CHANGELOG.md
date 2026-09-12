# Changelog

All notable public changes are documented here.

## 1.2.0 — 2026-09-12

- Added architecture guidance for Hierarchical Dual-Store RAG (Raw Corpus + SSoT Reports) with priority arbitration prompting.
- Documented quantitative benchmark results demonstrating significant accuracy gains (85.0% vs. 39.0% Naive Dense / 46.0% Hybrid Rerank) and an 83.3% reduction in context prompt overhead.
- Added synthetic walkthrough for dual-store ingestion and priority arbitration retrieval in EXAMPLE.md and EXAMPLE.zh-TW.md.
- Explicitly documented the security boundary for the evaluation suite (excluding live API keys, vector DB binaries, internal prompt logs, and un-anonymized benchmark datasets in compliance with institutional data governance and privacy requirements).
- Sanitized public configuration examples (.env.example).

## 1.1.0 — 2026-09-11

- Replaced unconditional latest-date overwrite guidance with scope-aware
  temporal and authority arbitration.
- Clarified that recency, structured formatting, and fresh context are not
  sufficient on their own to establish authority or model independence.
- Added explicit handling for unresolved scope and provenance conflicts.
- Updated the inventory guidance emitted by synthesize.py.
- Added English and Traditional Chinese public documentation.
- Replaced corpus-derived examples with synthetic examples.
- Added software citation metadata and an MIT license file.
- Corrected the docling-skill dependency to the published v1.2.1 tag and added uv.lock.
- Strengthened ignore rules for private research and manuscript artifacts.

## 1.0.0

- Initial public workflow for chronological document inventory, synthesis,
  image-placeholder review, RAG bundle creation, and post-synthesis audit.
