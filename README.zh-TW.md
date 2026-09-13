# doc-timeline-synthesizer

繁體中文 | [English](README.md)

這是一套重視出處鏈與範圍一致性的跨文件時序蒸餾工作流，用於把多版本文件整理成可稽核、可供檢索與決策支援的摘要。

本專案不把「日期最新」直接等同於「答案正確」。系統先確認候選值是否指向相同實體、屬性、期間、範圍、單位與欄位語意，再綜合文件狀態、簽核狀態、時間與出處判定權威性。證據不足時保留衝突，不強制產生單一答案。

## 架構設計

![多文件知識仲裁與治理流水線](docs/images/fig1_workflow.png)

本工作流將多文件知識蒸餾與治理拆解為四個核心階段：

1. **L1 — 實體轉換（Physical Ingestion，`docling-skill`）**：
   - 將 DOCX、PDF、XLSX、PPTX 等異質文件標準化轉為不可變的 `source.md`。
   - 保留結構化清單（`source.manifest.json`）與原始表格格位，嚴禁在 L1 階段進行具幻覺風險的就地篡改。
2. **Step Zero — 多模態邊車擴充（Multimodal Sidecar Enrichment，`scan_image_placeholders.py`）**：
   - 掃描並定位 `[[image:...]]` 佔位符，分派視覺模型專責辨識。
   - 檢驗並記錄略過非決策優先級圖片（如純商標、活動照片等，記錄於 `source.images.skip.json`），將決策關鍵之光柵圖表提取為獨立邊車檔案 `source.images.md`。
   - 嚴格維持 L1 輸出之不可變性（DEC-003）。
3. **L2 — 範圍感知蒸餾（Scope-Aware SSoT Distillation，`doc-timeline-synthesizer`）**：
   - 建立時間序列並分類四大衝突類型（時序覆蓋、公文內矛盾、統計範圍不一致、事實基線衝突）。
   - 依據公文核定效力、出處與簽核狀態判定權威性，而非粗糙的「新覆蓋舊」。
   - 產出具備逐項引用的單一真實來源（Single Source of Truth，SSoT）領域報告。
4. **L3 — 新脈絡審核（Fresh-Session Adversarial Audit，`doc-timeline-auditor`）**：
   - 在完全獨立、清空歷史記憶的 agent context 中，逆向檢驗 SSoT 報告與原始語料（DEC-002）。
   - 執行五維度對抗審核：引用可解析性、來源風險揭露、跨時戳拼接檢驗、抽樣覆蓋度、算術重新驗算。
   - 杜絕代理人自我強化之盲點與數值計算錯誤。

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

## 下游整合：分層雙庫 RAG（Hierarchical Dual-Store RAG）

![分層雙庫 RAG 架構圖](docs/images/fig2_dual_store_architecture.png)

為突破長文本記憶體限制並保證檢索決策之權威性，本架構提出**分層雙庫 RAG**：
- **Store 1（SSoT 權威總庫）**：收納經 L3 稽核之高層次領域 SSoT 報告（100 個區塊），賦予**高優先級（權威權限）**。
- **Store 2（原始佐證庫）**：收納細部未壓縮之原始公文區塊（4,655 個區塊），賦予**低優先級（情境與背景佐證）**。
- **並行混合分派與優先權仲裁 Prompting**：收到查詢後，以稠密向量（Dense BGE-M3）+ BM25 + 交叉編碼器重排（Cross-Encoder Reranker）並行檢索雙庫，取得平衡之 Top-5 + Top-5 區塊，並透過 Prompting 指令引導生成模型（`gemma-4-31B-it`）：遇數值或事實衝突時優先採信 SSoT 報告，同時保留原始公文之時序背景與佐證細節。

## 量化評測成果

![各題型準確率比較圖](docs/images/fig3_accuracy_comparison.png)

本工作流之下游檢索效益在涵蓋時序版本更新、多年度軌跡追蹤、跨實體陷阱與預算提案衝突之 100 題對抗基準測試中進行驗證：

| 檢索與上下文架構 | 自動回答匹配率 (Answer-Match Rate) | 提示詞上下文負擔 (Tokens) |
|:---|---:|---:|
| 單純密集向量檢索 Naive Dense RAG (僅原始公文, Top-5) | 39.0% | 約 1,750 tokens |
| 混合檢索 Hybrid RAG (BM25 + Dense) + BGE 重排 (Top-5) | 46.0% | 約 1,750 tokens |
| 全文基準 Full-Context (直接塞入完整 SSoT 報告) | **87.0%** | >21,000 tokens |
| **分層雙庫 RAG (原始公文 Top-5 + SSoT Top-5)** | **85.0%** | **約 3,500 tokens** |

分層雙庫設計展現了與全文檢索相當之匹配率（85.0% vs. 87.0%，McNemar 檢定 $p = 0.814$ 無顯著差異），同時大幅減少 **約 83%** 之提示詞上下文預算負擔（約 3,500 vs. >21,000 tokens 規劃預算），並顯著超越單庫標準 RAG ($p < 0.001$)。

### 殘餘未命中案例探索性質性診斷

![自動未命中案例探索性質性診斷](docs/images/fig4_failure_attribution.png)

針對分層雙庫 RAG（Condition 2）在自動化評測下未匹配之 15 題案例進行探索性質性診斷（Exploratory Non-Match Diagnostics），分類如下：

| 診斷分類 (Diagnostic Category) | 題數 ($N=15$) | 佔比 | 內容性質 | 診斷說明 |
|:---|:---:|:---:|:---:|:---|
| **潛在匹配或涵蓋率問題 (Potential Matching/Coverage)** | **13** | **86.7%** | 候選匹配 | 模型推導出核定數據與決策事實，因自然語言表面表達（如中文大寫金額單位、標點符號、Markdown 結構化條列清單）或回答清單不完整，超出嚴格字串比對正則範圍。 |
| **已檢索證據未被回答使用 (QA-INTRA-019)** | 1 | 6.7% | 細節未引用 | 檢索出之原始 chunk 已包含 099 案凍結金額（800 萬元）與期限（3 個月），但模型生成時遺漏輸出該數值。 |
| **標準答案包含未提問要求 (Unasked Gold-Answer Requirement, QA-INTRA-020)** | 1 | 6.7% | 評分標準過苛 | 題幹詢問解凍條件，標準答案評分規則卻預期未在題幹中提示之特定金額門檻（1,000 萬元）。 |

**關鍵診斷重點：**
- **主要正式指標：** 論文以 **85.0% 自動回答匹配率（Automated Answer-Match Rate）** 作為唯一正式、預先指定之指標，以維護嚴格可重現的跨系統統計比較。在缺乏多位獨立評審雙盲標註的情況下，不另行宣告 98% 語意正確率。
- **自動化陷阱標記與衝突化解率澄清（$STER = 12.0\%$, $CRR = 73.0\%$）：** 依定義 $CRR = Acc \land \neg Trap$（$85.0\% - 12.0\% = 73.0\%$），自動化 CRR 得分反映了 12 筆自動化陷阱標記。經核查，其中 4 筆為專案代號前綴 `CP11501-00` 碰撞；8 筆為歷史比較情境。模型絕大多數皆確立核定數據，但邊界案例（如 QA-TEMPORAL-002 輸出成長區間「37.7% 至 41.8%」）仍有殘留數值污染。因此 STER 與 CRR 均保留作為客觀保守的確定性檢測器基準。

## 安全與資料邊界

公開 repo 只包含通用工作流與工具，不包含研究語料、內部行政文件、原始對話、逐筆研究 ledger 或論文 supplement。

依據研究機構資料治理與倫理合規要求：
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
