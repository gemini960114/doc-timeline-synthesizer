# Synthetic end-to-end example

[繁體中文](EXAMPLE.zh-TW.md) | English

This walkthrough uses fabricated filenames and values. It contains no research
corpus content.

## 1. Prepare isolated local data

    mkdir -p data/example_domain
    mkdir -p output/example_domain
    mkdir -p reports

Example documents:

    data/example_domain/
      2025-01-10_initial_plan.docx
      2025-03-15_approved_revision.pdf
      2025-04-02_status_note.xlsx

These directories are ignored by Git and must remain local.

## 2. Run L1 conversion

Use docling-skill to create one output folder per source document. Each folder
should contain source.md and, when available, source.manifest.json and
source.evidence.json.

## 3. Check embedded images

    uv run python scripts/scan_image_placeholders.py       --input-dir output/example_domain

If an image contains decision-relevant evidence, describe it in
source.images.md with a pointer to the original placeholder. If it is only a
logo or decorative image, record a reasoned skip marker rather than silently
ignoring it.

## 4. Build the chronological inventory

    uv run python scripts/synthesize.py       --input-dir output/example_domain       --output-file output/example_domain_inventory.md

The inventory is a diagnostic index, not the final evidence base. The agent
must still read every relevant source file in full.

## 5. Run scope-aware synthesis

Suggested prompt:

    Read output/example_domain_inventory.md and every source.md, manifest,
    and relevant image sidecar under output/example_domain. Create a
    citation-backed summary using SKILL.md. Compare candidate values only
    when entity, attribute, period, scope, unit, and semantics match.
    Consider recency together with provenance, document status, and approval
    state. Keep unresolved conflicts explicit. Save the result as
    reports/example_domain_summary.md.

Synthetic conflict example:

- A draft dated 2025-01-10 reports a planned capacity of 100 units.
- An approved revision dated 2025-03-15 reports 112 units for the same site,
  period, and definition.
- A status note dated 2025-04-02 reports 118 units but includes an additional
  site.

The third value is newer but not directly comparable. A valid summary can
select 112 units for the original scope and separately disclose the broader
118-unit scope. It must not overwrite 112 solely because 118 is newer.

Synthetic intra-document example:

- Narrative text says 40 units.
- An operative approved field says 4 units.
- A template comparison shows that the narrative was copied from another
  form.

The structured value may be selected in this specific case because its
authority is supported by document status, field purpose, and corroborating
evidence. This does not create a universal structured-data priority.

## 6. Run the L3 audit

Start a fresh agent context. Provide the finished report path and original
source directory, but not the producer's conversation history or reasoning
trace.

Suggested prompt:

    Use doc-timeline-auditor/SKILL.md to audit
    reports/example_domain_summary.md against output/example_domain.
    Resolve every citation, inspect source-risk metadata, test for
    cross-version splicing, sample omitted content, recompute arithmetic,
    and verify statistical scope. Return PASS, PASS WITH CAVEATS, or FAIL
    with evidence for each finding.

## 7. Build RAG files

    uv run python scripts/build_rag_bundle.py       --input-dir output/example_domain

Index source.rag.md rather than source.md when image sidecars are present.

## 8. Ingest into Hierarchical Dual-Store RAG (Synthetic example)

To balance granular document context with audited consensus authority, maintain
two distinct vector or hybrid collections:

1. **`raw_corpus` collection**: Ingest chunked `source.rag.md` files from `output/`.
2. **`ssot_reports` collection**: Ingest chunked domain reports from `reports/`.

When querying:
- Query both collections simultaneously (e.g., retrieve Top-5 chunks from `raw_corpus`
  and Top-5 chunks from `ssot_reports`).
- Use a priority arbitration system prompt:
  > "You are answering questions using two knowledge sources: [SSOT_REPORTS]
  > (audited, scope-verified domain summaries) and [RAW_CORPUS] (detailed source
  > documents). If any numerical, factual, or temporal conflict exists between
  > them, prioritize the values in [SSOT_REPORTS] as authoritative, while citing
  > relevant historical progression from [RAW_CORPUS]."

This prevents superseded drafts in the raw corpus from misleading the generator
while preserving rich circumstantial evidence.

## 9. Release check

Before sharing any output:

- confirm that the source owner permits publication;
- remove identifiers and restricted content;
- obtain human verification of consequential values;
- inspect the exact files staged for Git;
- keep raw documents, evaluation datasets, vector databases, and generated reports outside the public repository.
