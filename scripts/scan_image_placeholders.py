#!/usr/bin/env python3
"""Image Placeholder Scanner for doc-timeline-synthesizer.

docling-skill (L1) does not describe embedded image content by default; it
leaves a stable `[[image:picture-id]]` token in source.md and stores the raw
image as base64 in source.evidence.json. This script does NOT describe image
content itself (that requires an LLM with vision) -- it only detects which
source folders still carry unresolved placeholders and reports enough
context (risk_level, character count, existing enrichment/skip status) for a
human or Agent to decide whether Step Zero (Picture Placeholder Enrichment,
see SKILL.md) is worth running for each one.

Decision records:
  - `source.images.md`        -> a real description was written (Step Zero done)
  - `source.images.skip.json` -> a human/Agent deliberately decided the image(s)
                                  carry no decision-relevant content, so
                                  doc-timeline-auditor should not flag it as
                                  "unresolved citation" later.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\[\[image:([\w\-]+)\]\]")

STATUS_ICON = {"待處理": "⚠", "已補強": "✔", "已略過": "○"}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def scan_folder(folder: Path) -> dict | None:
    md_file = folder / "source.md"
    if not md_file.exists():
        return None
    text = md_file.read_text(encoding="utf-8")
    placeholders = PLACEHOLDER_RE.findall(text)
    if not placeholders:
        return None

    manifest = load_json(folder / "source.manifest.json")
    risk_level = manifest.get("decision", {}).get("risk_level", "unknown")
    char_count = manifest.get("counts", {}).get("characters", len(text))

    images_md = folder / "source.images.md"
    skip_marker = folder / "source.images.skip.json"

    if images_md.exists():
        status, detail = "已補強", ""
    elif skip_marker.exists():
        info = load_json(skip_marker)
        status = "已略過"
        detail = f"({info.get('date', '?')}, {info.get('reason', '未附理由')})"
    else:
        status, detail = "待處理", ""

    return {
        "name": folder.name,
        "placeholders": placeholders,
        "risk_level": risk_level,
        "char_count": char_count,
        "status": status,
        "detail": detail,
    }


def mark_skip(input_path: Path, folder_name: str, reason: str) -> None:
    target = input_path / folder_name
    if not target.exists():
        print(f"❌ Error: folder not found: {target}")
        sys.exit(1)
    marker = target / "source.images.skip.json"
    marker.write_text(
        json.dumps(
            {"decision": "skip", "date": date.today().isoformat(), "reason": reason or "未附理由"},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"✔ 已記錄略過決定: {target.name} -> {marker}")


def main():
    parser = argparse.ArgumentParser(
        description="Scan for unresolved docling-skill image placeholders and report Step Zero enrichment status"
    )
    parser.add_argument(
        "--input-dir",
        default="./output",
        help="Domain output directory to scan, e.g. output/01_財會預算 (default: ./output)",
    )
    parser.add_argument(
        "--mark-skip",
        metavar="FOLDER_NAME",
        help="Record that a specific source folder's image(s) were deliberately judged out of scope (writes source.images.skip.json)",
    )
    parser.add_argument(
        "--reason",
        default="",
        help="Reason to record with --mark-skip, e.g. '僅版頭/簽章圖，無決策數字'",
    )
    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    if not input_path.exists():
        print(f"❌ Error: input directory does not exist: {input_path}")
        sys.exit(1)

    if args.mark_skip:
        mark_skip(input_path, args.mark_skip, args.reason)
        return

    folders = sorted(f for f in input_path.iterdir() if f.is_dir())
    results = [r for r in (scan_folder(f) for f in folders) if r]

    print(f"📷 圖片佔位符掃描: {input_path.name}")
    print(f"   共 {len(folders)} 份文件，{len(results)} 份含圖片佔位符\n")

    if not results:
        print("   ✔ 無圖片佔位符，可直接跳過步驟零。")
        return

    pending = done = skipped = 0
    for r in results:
        icon = STATUS_ICON[r["status"]]
        print(
            f"   {icon} {r['name']}  "
            f"({len(r['placeholders'])}張圖, risk_level: {r['risk_level']}, {r['char_count']:,}字)  "
            f"狀態: {r['status']} {r['detail']}"
        )
        if r["status"] == "待處理":
            pending += 1
        elif r["status"] == "已補強":
            done += 1
        else:
            skipped += 1

    print(f"\n   待處理: {pending} 份 | 已補強: {done} 份 | 已略過: {skipped} 份")
    if pending:
        print("\n   建議：優先處理 risk_level 較高、或字元數偏少（代表文字內容可能不足以佐證圖片內數字）者。")
        print("   對已確認不重要的圖片（例如版頭/簽章圖），記錄略過決定：")
        print(f'   python3 {Path(__file__).name} --input-dir {args.input_dir} --mark-skip <資料夾名稱> --reason "..."')


if __name__ == "__main__":
    main()
