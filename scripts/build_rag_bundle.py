#!/usr/bin/env python3
"""RAG Bundle Builder for doc-timeline-synthesizer.

Merges each source folder's canonical `source.md` (L1 docling-skill output)
with its optional `source.images.md` (Step Zero image-placeholder
enrichment sidecar, see SKILL.md) into a single `source.rag.md` file --
the one file a RAG ingestion pipeline should actually point at.

This never modifies `source.md` or `source.images.md`. `source.rag.md` is a
disposable, regenerable artifact: re-run this script any time either input
changes, and re-index it in your RAG system afterward.
"""

import argparse
import sys
from pathlib import Path

OUT_NAME = "source.rag.md"


def build_folder(folder: Path) -> bool:
    md = folder / "source.md"
    if not md.exists():
        return False

    text = md.read_text(encoding="utf-8")
    images_md = folder / "source.images.md"
    if images_md.exists():
        text = (
            text.rstrip()
            + "\n\n---\n\n"
            + "## 圖片內容補充說明（Step Zero 圖片佔位符補強）\n\n"
            + images_md.read_text(encoding="utf-8").rstrip()
            + "\n"
        )

    (folder / OUT_NAME).write_text(text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build source.rag.md (source.md + source.images.md merged) for RAG ingestion"
    )
    parser.add_argument(
        "--input-dir",
        default="./output",
        help="Domain output directory to process, e.g. output/01_財會預算 (default: ./output)",
    )
    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    if not input_path.exists():
        print(f"❌ Error: input directory does not exist: {input_path}")
        sys.exit(1)

    folders = sorted(f for f in input_path.iterdir() if f.is_dir())
    built = merged = 0
    for folder in folders:
        if build_folder(folder):
            built += 1
            if (folder / "source.images.md").exists():
                merged += 1

    print(f"✔ 已產出 {built} 份 {OUT_NAME}（{input_path.name}），其中 {merged} 份含圖片補強內容")
    print(f"  RAG 上傳請指向: {input_path}/**/{OUT_NAME}（不要直接指向 source.md）")


if __name__ == "__main__":
    main()
