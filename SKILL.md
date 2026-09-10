---
name: doc-timeline-synthesizer
description: Use when an agent needs to perform multi-document chronological deduplication, denoising, timeline conflict resolution, and knowledge synthesis across docling-skill source.md outputs to produce a clean, citation-backed Single Source of Truth for RAG, NotebookLM, or executive briefings.
---

# doc-timeline-synthesizer

`doc-timeline-synthesizer` 是面向 AI Agent 的**跨文檔時序聚合與知識蒸餾層（L2 Synthesis Layer）**。
它銜接 `docling-skill`（L1 Ingestion Layer）產出的 `source.md` 檔案集合，透過時間軸排序、語意去雜訊、跨文檔去重與版本覆寫機制，產出唯一、具備出處佐證（Citation-backed）的「最新拍板單一真相（Single Source of Truth, SSOT）」。

## 流水線架構（Pipeline Architecture）

```
[原始各類文件] 
      │
      ▼
【docling-skill】(L1) ── 單文檔物理排版解析、清洗 CJK 字距，產出 output/*/source.md
      │
      ▼
【doc-timeline-synthesizer】(L2) ── 跨文檔時序排序、語意聚合、新舊衝突裁決，產出《總整理.md》
      │
      ▼
【下游應用】 ── 高精準 RAG 知識庫 / NotebookLM / 首長決策簡報
```

> [!NOTE]
> **工具與大腦分工**：
> 內建腳本 `scripts/synthesize.py` 負責**文檔清單時序排序、品質健檢與指標片段初篩**；真正的高階語意去雜訊、跨文檔實體提煉與新舊數值覆寫裁決，是由 **LLM Agent** 依據本規範執行。

---

## 領域驅動分類與目錄隔離架構（Domain-Driven Segmentation）

為避免不同業務領域（如「財務數字」與「行政公文」）互相干擾造成檢索污染，建議採取專題目錄分流：

```text
data/ （原始檔案分類放置）
├── 01_財會預算/   <--- 預算書、歲出概況表、經費執行數
├── 02_立院與行政/ <--- 立委對案、部會函文、公文簽呈、模擬題庫
└── 03_計畫與技術/ <--- 綱要計畫書、核心技術規格、研發進度報告

output/ （各自獨立累積與蒸餾）
├── 01_財會預算/   ---> 產出專屬【財會預算_最新拍板總整理.md】
├── 02_立院與行政/ ---> 產出專屬【立院與行政_最新拍板總整理.md】
└── 03_計畫與技術/ ---> 產出專屬【技術研發_最新拍板總整理.md】
```

### 領域隔離原則：
1. **業務解耦**：財會只處理經費、保留數與資本門；行政只處理管考、立委質詢與責任歸屬。
2. **滾動累積**：新文件依屬性歸入各自的專題資料夾，各資料夾內的 `source.md` 持續累積，增量更新時互不干擾。
3. **金字塔匯總（Meta-Synthesis）**：當需要全局戰略簡報時，直接合併各領域的《總整理.md》（各約 2,000 字），幾秒鐘即可完成跨域綜整。

---

## 核心處理原則（Core Principles）

### 1. 物理與行政去雜訊（Denoising）
自動忽略下列無決策價值的樣板行政文字：
- 公文條例抬頭、收發文號、會簽流程文字、承辦人分機號碼。
- 每一份公文開頭千篇一律的背景宣示（例如「因應國際科技發展趨勢...」）。

### 2. 五大實體萃取維度（5D Extraction Schema）
對每份文件以結構化維度提取核心事實：
1. **專案實體（Project Entities）**：計畫名稱、統一編號、主辦與執行單位。
2. **關鍵人物與關係人（Stakeholders）**：計畫主持人、提案委員、業務聯繫窗口。
3. **量化數據指標（Metrics）**：全程經費、年度法定預算、年度需求額度、關鍵技術指標、完工時程。
4. **爭議與痛點（Concerns）**：時程是否落後、預算重疊質疑、資安疑慮、產業落地效益。
5. **官方拍板對策（Official Actions）**：過渡期調度措施、法規鬆綁、試用成效與里程碑。

### 3. 時間序衝突覆寫法則（Latest-Date Overwrite Rule）
- **時間排序**：抓取檔名或內文中的年月日時間戳（如 `1150828` > `1150720` > `1150601`）。
- **單一真相**：當同一指標出現不同數據時，**最新時間戳記的數值直接覆寫舊數據，作為唯一主事實（Latest Truth）**。
- **出處標註（Provenance / Citation）**：每個關鍵數字（預算、時程、規格）均須在後方註記出處來源檔名及章節表號，便於人工抽查審計。
- **沿革保留**：被推翻的舊提法或早期預估，僅保留為決策演進脈絡（History），絕不與新數據並列為主數據。
- **禁止跨時間戳拼接（Anti-Splicing Rule）**：同一指標若由多個計量單位共同描述（例如「電力規模 MW」與「算力 PF/儲存 PB」常成組出現），**必須確認每一個單位都來自同一份、同一時間戳的文件**，嚴禁把舊時間戳文件的某個單位數值，與新時間戳文件的另一個單位數值拼接成同一句主張。若新文件只更新了部分單位（例如只更新 PF 未提及 MW），應標註「該單位尚未見更新版本」，而非沿用舊文件的對應數值冒充最新資料。

---

## 標準執行步驟（Execution Steps）

### 步驟一：呼叫預備健檢與時序排序腳本
```bash
python3 scripts/synthesize.py --input-dir "./output" --output-file "chronological_inventory.md"
```
* 腳本將產出時序總表、字元數統計、文件品質狀態，並顯式列出未定時間（UNDATED）之文件以供人工檢視。

### 步驟二：LLM 認知蒸餾與報告撰寫
Agent 讀取 `chronological_inventory.md` 與各關鍵文檔，依據本規範執行：
1. 建立「單一真相數據速查表」，標記出處來源。
2. 將各計畫依主題分組，清楚區隔【最新拍板現況】與【質疑及演進時間軸】。
3. 杜絕新舊數值混淆，大幅降低 RAG 與下游應用的幻覺風險。

> [!IMPORTANT]
> `chronological_inventory.md` 之「關鍵指標初篩片段」僅為每份文件開頭數百字的截斷預覽，**不可作為蒸餾之唯一依據**。對字元數龐大（如超過 5 萬字）之 `source.md`（常見於綱要計畫書、歲出概況表等），Agent 必須完整讀畢全文，逐一核對文件中所有指標版本，才能執行步驟三。僅依賴片段摘要進行蒸餾，是導致「新舊數值混拼」與「指標漏抓」的主要成因。

### 步驟三：抽樣回溯驗證（Spot-Check Verification）
報告初稿完成後，Agent 須自行執行以下品管動作，作為蒸餾完工的必要條件（而非選配）：
1. 從《總整理.md》的「單一真相數據速查表」與「深度剖析」章節中，隨機抽取至少 5-8 個具體數字（優先挑選成組出現的多單位指標，例如「MW／PF／PB」同時出現的敘述）。
2. 針對每個抽樣數字，回頭以文字檢索（grep 或全文搜尋）比對其來源 `source.md`，確認數值、單位與時間戳三者皆正確對應，且未違反上述「禁止跨時間戳拼接」原則。
3. 若報告涉及跨領域彙整（金字塔匯總），必須額外確認：來源《總整理.md》中的錯誤是否被原樣複製擴散到匯總簡報，避免同一錯誤重複出現於多份文件。
4. 將驗證結果（已核實通過 / 發現並修正）簡要列於報告交付紀錄或對話回覆中，作為品質佐證；不得在未完成抽查的情況下逕自宣稱「重點已涵蓋」。

---

## 交付成果規格（Output Contract）

生成的總整理文件應符合以下章節結構：
1. **壹、核心計畫「最新單一真相」數據速查表（含出處標籤）**
2. **貳、領域重點數據與既有量能盤點**
3. **參、各關鍵主題深度剖析**（最新定案 / 爭議焦點 / 時間演進 Changelog）
4. **肆、下游 RAG 與 NotebookLM 引用指引**
