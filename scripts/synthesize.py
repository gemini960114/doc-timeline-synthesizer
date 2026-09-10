#!/usr/bin/env python3
"""Chronological Pre-Synthesis and Inventory Tool for doc-timeline-synthesizer.

This script scans docling-skill output directories, extracts timestamps, performs
diagnostics on manifest quality signals, flags undated/anomalous files, and outputs
a structured Chronological Pre-Synthesis Manifest to assist LLM-driven synthesis.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_timestamp(name: str) -> tuple[str, bool]:
    """Extract Taiwan (ROC) or Western date from folder/file name.
    
    Returns:
        (parsed_date_str, is_valid)
    """
    # 1. Matches 7-digit Taiwan date (e.g. 1150601, 1150720, 1150828)
    m1 = re.search(r'(?<!\d)(11\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)', name)
    if m1:
        return f"{m1.group(1)}{m1.group(2)}{m1.group(3)}", True

    # 2. Matches 8-digit Western date (e.g. 20260601, 2026-09-04)
    m2 = re.search(r'(?<!\d)(202\d)[-_]?(0[1-9]|1[0-2])[-_]?(0[1-9]|[12]\d|3[01])(?!\d)', name)
    if m2:
        return f"{m2.group(1)}{m2.group(2)}{m2.group(3)}", True

    # 3. Matches dates with dot/slash/hyphen: 115.08.14, 115/06/01
    m3 = re.search(r'(?<!\d)(11\d)[.\-/](0?[1-9]|1[0-2])[.\-/](0?[1-9]|[12]\d|3[01])(?!\d)', name)
    if m3:
        return f"{m3.group(1)}{int(m3.group(2)):02d}{int(m3.group(3)):02d}", True

    return "999999_UNDATED", False


def extract_key_metrics_snippets(text: str, max_snippets: int = 5) -> list[str]:
    """Find lines mentioning budgets, dates, milestones, or compute power."""
    keywords = ["預算", "經費", "算力", "PFLOPS", "MW", "PUE", "時程", "完工", "主機"]
    snippets = []
    for line in text.splitlines():
        line_clean = line.strip()
        if len(line_clean) < 10 or line_clean.startswith("#"):
            continue
        if any(k in line_clean for k in keywords):
            # clean markdown formatting slightly
            cleaned = re.sub(r'\s+', ' ', line_clean)
            if cleaned not in snippets:
                snippets.append(cleaned[:120])
                if len(snippets) >= max_snippets:
                    break
    return snippets


def main():
    parser = argparse.ArgumentParser(
        description="Pre-synthesis diagnostics and chronological inventory for doc-timeline-synthesizer"
    )
    parser.add_argument(
        "--input-dir",
        default="./output",
        help="Directory containing docling-skill output subfolders (default: ./output)",
    )
    parser.add_argument(
        "--output-file",
        default="chronological_inventory.md",
        help="Path for generated pre-synthesis manifest file",
    )
    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    if not input_path.exists():
        print(f"❌ Error: input directory does not exist: {input_path}")
        sys.exit(1)

    folders = [f for f in input_path.iterdir() if f.is_dir() and f.name != "test_doc"]
    if not folders:
        print(f"⚠️ Warning: No subfolders found in {input_path}")
        return

    dated_items = []
    undated_items = []

    for f in folders:
        md_file = f / "source.md"
        manifest_file = f / "source.manifest.json"

        if not md_file.exists():
            continue

        ts, is_valid = parse_timestamp(f.name)
        text = md_file.read_text(encoding="utf-8")
        
        manifest_data = {}
        if manifest_file.exists():
            try:
                manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        quality_status = manifest_data.get("decision", {}).get("status", "unknown")
        risk_level = manifest_data.get("decision", {}).get("risk_level", "unknown")
        snippets = extract_key_metrics_snippets(text)

        item = {
            "name": f.name,
            "timestamp": ts,
            "valid_date": is_valid,
            "char_count": len(text),
            "status": quality_status,
            "risk": risk_level,
            "snippets": snippets,
            "path": str(md_file),
        }

        if is_valid:
            dated_items.append(item)
        else:
            undated_items.append(item)

    # Sort dated items chronologically (oldest to newest)
    dated_items.sort(key=lambda x: (x["timestamp"], x["name"]))

    print(f"📊 掃描完成: 總計 {len(dated_items) + len(undated_items)} 份文檔")
    print(f"   已識別時間戳: {len(dated_items)} 份")
    if dated_items:
        print(f"   時間跨度: {dated_items[0]['timestamp']} -> {dated_items[-1]['timestamp']}")

    if undated_items:
        print(f"⚠️  警告: 發現 {len(undated_items)} 份未識別明確時間戳的文件（需人工指定時間權重）:")
        for u in undated_items:
            print(f"   - {u['name']}")

    # Write out the Chronological Pre-Synthesis Inventory
    out_path = Path(args.output_file).resolve()
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("# 文檔時序預備盤點清單（Chronological Pre-Synthesis Inventory）\n\n")
        out.write(f"> **掃描目錄**：`{input_path}`  \n")
        out.write(f"> **文件總數**：{len(dated_items) + len(undated_items)} 份（有效時間序: {len(dated_items)}，未定時間: {len(undated_items)}）  \n")
        out.write(f"> **時間範圍**：{dated_items[0]['timestamp'] if dated_items else 'N/A'} 至 {dated_items[-1]['timestamp'] if dated_items else 'N/A'}\n\n")
        out.write("---\n\n")

        out.write("## 壹、時序排序總表（由舊至新，後者覆寫前者）\n\n")
        out.write("| 序號 | 時間戳 (Timestamp) | 文檔資料夾名稱 | 字元數 | Ingestion品質 | 關鍵指標初篩片段 |\n")
        out.write("| :---: | :---: | :--- | :---: | :---: | :--- |\n")
        
        for idx, item in enumerate(dated_items, 1):
            snippet_str = "<br>• ".join(item["snippets"][:2]) if item["snippets"] else "無顯著數值片段"
            out.write(f"| {idx} | **{item['timestamp']}** | `{item['name']}` | {item['char_count']:,} | {item['status']} ({item['risk']}) | • {snippet_str} |\n")

        if undated_items:
            out.write("\n## 貳、未識別日期文檔（需人工審查或補充時間戳記）\n\n")
            out.write("| 文檔資料夾名稱 | 字元數 | 品質狀態 | 檔案路徑 |\n")
            out.write("| :--- | :---: | :---: | :--- |\n")
            for u in undated_items:
                out.write(f"| `{u['name']}` | {u['char_count']:,} | {u['status']} ({u['risk']}) | `{u['path']}` |\n")

        out.write("\n---\n\n")
        out.write("## 參、LLM 認知蒸餾指示（Instructions for Agent Synthesis）\n")
        out.write("請 Agent 依據此時序清單與 `SKILL.md` 規範執行：\n")
        out.write("1. **嚴格時間序覆寫**：針對同一計畫指標，後發布時間點（較大序號）數值直接覆寫舊時間點數值，定案為 Latest Truth。\n")
        out.write("2. **出處標註**：每個關鍵數字（預算、算力、時程）必須標註其來自之具體資料夾及章節表號，嚴禁脫離證據生成。\n")
        out.write("3. **去除行政贅詞**：忽略公文表頭、簽核代碼、問候語與樣板前言。\n")

    print(f"✔ 成功產出時序預備盤點檔案: {out_path}")


if __name__ == "__main__":
    main()
