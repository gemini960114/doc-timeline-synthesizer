# doc-timeline-synthesizer

繁體中文 | [English](README.md)

這是一套重視出處鏈與範圍一致性的跨文件時序蒸餾工作流，用於把多版本文件整理成可稽核、可供檢索與決策支援的摘要。

本專案不把「日期最新」直接等同於「答案正確」。系統先確認候選值是否指向相同實體、屬性、期間、範圍、單位與欄位語意，再綜合文件狀態、簽核狀態、時間與出處判定權威性。證據不足時保留衝突，不強制產生單一答案。

## 架構設計

1. L1 — 實體轉換
   - 將 DOCX、PDF、XLSX、PPTX 等文件轉成 source.md。
   - 保留 docling-skill 產生的 manifest 與 evidence。
2. L2 — 範圍感知蒸餾
   - 建立時間序。
   - 移除重複樣板文字。
   - 只在範圍相容、證據充分時進行版本仲裁。
   - 產生逐項附出處的領域總整理。
3. L3 — 新脈絡審核
   - 以新的 agent context 逆向檢查成品與原始語料。
   - 不提供 L2 的對話歷史或推理軌跡。
   - 檢查引用、來源風險、跨版本拼接、覆蓋度、算術與統計範圍。
   - 新脈絡分離不等同於不同模型家族的獨立性。
4. 下游整合 — 分層雙庫 RAG（Hierarchical Dual-Store RAG）
   - 將細部原始文件（`source.rag.md`）與經稽核的 SSoT 報告（`reports/*.md`）分置於兩個獨立向量/混合集合。
   - 查詢時兩庫並行檢索，並透過優先權仲裁 Prompting 指引生成模型：遇數值或事實衝突時優先採信 SSoT 報告，同時保留原始公文之時序背景與佐證細節。

## 核心規則

- 先比對範圍，再比較日期。
- 新近性只是權威判斷因素之一，不是無條件覆寫規則。
- 不預設表格或結構化欄位永遠優於敘述文字。
- 每個重要主張記錄來源、日期、章節或表格，以及採信理由。
- 權威性不足時明確保留衝突。
- 不可拼接來自不相容版本的單位或屬性。
- 判定「查無出處」前，先處理圖片佔位符。
- 高風險摘要在交付前應接受新脈絡審核。
- 在下游 RAG 整合中，將原始文件與經稽核之 SSoT 報告分庫儲存，並實施優先權仲裁 Prompting。

## 安裝

建議使用 Python 3.10 以上與 uv：

    git clone https://github.com/gemini960114/doc-timeline-synthesizer.git
    cd doc-timeline-synthesizer
    uv sync

L1 轉換依賴 pyproject.toml 宣告的 docling-skill。

## 快速開始

把來源文件放在已排除版本控制的本機資料夾：

    data/
      example_domain/
        2025-01-10_initial_plan.docx
        2025-03-15_approved_revision.pdf

完成 L1 轉換後建立時序盤點：

    uv run python scripts/synthesize.py       --input-dir output/example_domain       --output-file output/example_domain_inventory.md

掃描尚未處理的圖片佔位符：

    uv run python scripts/scan_image_placeholders.py       --input-dir output/example_domain

接著使用 SKILL.md 進行範圍感知蒸餾，並在新的 agent context 中掛載
doc-timeline-auditor/SKILL.md 進行 L3 審核。建立 RAG 輸入檔：

    uv run python scripts/build_rag_bundle.py       --input-dir output/example_domain

完整合成案例請見 EXAMPLE.zh-TW.md。

## 量化評測成果

本工作流之下游檢索效益在涵蓋時序版本更新、多年度軌跡追蹤、跨實體陷阱與預算提案衝突之 100 題對抗基準測試中進行驗證：

| 檢索與上下文架構 | 準確率 (Accuracy) | 提示詞上下文負擔 (Tokens) |
|:---|---:|---:|
| 單純密集向量檢索 Naive Dense RAG (僅原始公文, Top-5) | 39.0% | 約 1,750 tokens |
| 混合檢索 Hybrid RAG (BM25 + Dense) + BGE 重排 (Top-5) | 46.0% | 約 1,750 tokens |
| 全文基準 Full-Context (直接塞入完整 SSoT 報告) | **87.0%** | >21,000 tokens |
| **分層雙庫 RAG (原始公文 Top-5 + SSoT Top-5)** | **85.0%** | **約 3,500 tokens** |

分層雙庫設計展現了與全文檢索相當之準確率（85.0% vs. 87.0%，McNemar 檢定 $p = 0.814$ 無顯著差異），同時大幅減少 **83.3%** 之提示詞 Token 負擔，並顯著超越單庫標準 RAG ($p < 0.001$)。

## 安全與資料邊界

公開 repo 只包含通用工作流與工具，不包含研究語料、內部行政文件、原始對話、逐筆研究 ledger 或論文 supplement。

依據研究機構資料治理與倫理合規要求（ISS-06）：
- `evaluation/` 資料夾包含本機評測腳本與環境配置。
- 所有即時 API 金鑰（`evaluation/.env`）、本機虛擬環境（`evaluation/.venv/`）與二進位向量資料庫（`evaluation/chroma_db/`）皆已透過 `.gitignore` 嚴格排除。
- 未去識別化之內部評測題目集（`evaluation/benchmark/`）與執行過程之 Prompt/生成紀錄（`evaluation/results/`）包含機敏行政案例，嚴禁推送到公開儲存庫。

每次推送前應檢查實際 staged tree：

    git status --short
    git diff --cached
    git ls-files

不可提交 API key、token、本機絕對路徑、來源文件、evidence payload、向量資料庫或產出報告。

## 可重現性邊界

本 repo 可供檢視與重用通用方法，但不是任何使用私有或受限文件之研究的完整 replication package。特定語料的結果仍需另行取得公開授權並由作者人工確認。

## 引用與授權

若您在研究中使用本專案或引用相關方法，請引用我們的預印本論文：

```bibtex
@article{chuang2026resolving,
  title   = {Resolving Knowledge Conflicts in Versioned Documents with Hierarchical Dual-Store RAG},
  author  = {Chuang, Chao-Chun and Yao, Chih-Min and Lee, Tsui-Mei and Liu, Yi-Ni},
  journal = {arXiv preprint},
  year    = {2026},
  url     = {https://github.com/gemini960114/doc-timeline-synthesizer}
}
```

機器可讀之引用詮釋資料請參見 [CITATION.cff](file:///home/ubuntu/github/doc-timeline-synthesizer/CITATION.cff)。取得正式 arXiv ID 與 DOI 後將同步更新。

本專案採 MIT License，詳見 LICENSE。
