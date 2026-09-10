# doc-timeline-synthesizer

`doc-timeline-synthesizer` 是一個面向 AI Agent 的**跨文檔時序聚合與知識蒸餾層（L2 Synthesis Layer）**。

它銜接 [Docling](https://github.com/docling-project/docling) 與 [docling-skill](https://github.com/realraelrr/docling-skill)（L1 Ingestion Layer）所產出的多份標準 `source.md` 檔案，透過時間軸排序、語意去雜訊、跨文檔去重與新舊衝突覆寫，產出具備出處佐證（Citation-backed）的「最新拍板單一真相（Single Source of Truth, SSOT）」。

## 流水線架構

```text
[ 原始異質文件 (Word, PDF, Excel...) ]
                 │
                 ▼ (L1: Ingestion)
          【docling-skill】
   單文檔結構化解析、清洗 CJK 字距
        產出 output/*/source.md
                 │
                 ▼ (L2: Synthesis)
    【doc-timeline-synthesizer】
   跨文檔時序排序、語意去雜訊、新舊覆寫
      產出《最新拍板總整理.md》
                 │
                 ▼
[ 下游 RAG 知識庫 / NotebookLM / 決策簡報 ]
```

## 安裝與使用

```bash
# 安裝依賴（含 docling-skill）
uv sync

# 執行時序預備健檢與排序腳本
python3 scripts/synthesize.py --input-dir "./output" --output-file "chronological_inventory.md"
```

## Agent Skill 整合

本倉庫根目錄下的 `SKILL.md` 即為 Agent 技能定義檔。可透過軟連結掛載至常用的 Agent 環境：

```bash
# Claude Code
ln -sf /path/to/doc-timeline-synthesizer ~/.claude/skills/doc-timeline-synthesizer

# Codex
ln -sf /path/to/doc-timeline-synthesizer ~/.codex/skills/doc-timeline-synthesizer

# Antigravity / Gemini CLI
ln -sf /path/to/doc-timeline-synthesizer ~/.gemini/config/skills/doc-timeline-synthesizer
```
