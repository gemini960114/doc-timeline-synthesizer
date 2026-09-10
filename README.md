# doc-timeline-synthesizer

> **面向 AI Agent 的跨文檔時序聚合、衝突裁決與知識蒸餾層（L2 Synthesis Layer）**  
> 專為解決企業與公部門文檔多版次演進中「新舊數值混淆、會議質詢干擾、RAG 檢索幻覺」而設計的單一真相（SSOT）建構方案。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docling](https://img.shields.io/badge/Powered%20by-Docling-orange.svg)](https://github.com/docling-project/docling)
[![L1 Ingestion](https://img.shields.io/badge/Upstream-docling--skill-green.svg)](https://github.com/realraelrr/docling-skill)

---

## 📖 為什麼需要 doc-timeline-synthesizer？

在政府機關、大型企業或科技專案的推動過程中，非結構化文檔往往歷經**數個月、多個單位的往返修訂**（例如：預算概算書初稿、跨部會公文簽呈、質詢模擬答辯、期中考評報告、最終歲出分配定案）。

若將這些異質文件直接輸入給傳統 RAG 向量資料庫或大語言模型，常會發生嚴重的**跨文檔衝突與知識幻覺**：
- ❌ **數字矛盾與幻覺**：檢索系統同時撈出「6 月份提報的概算 12 億」與「8 月份最終拍板的 9.8 億」，AI 無法判讀何者為法定最新定案。
- ❌ **行政樣板雜訊**：大量收發文號、會簽代碼、公文樣板前言稀釋了具有決策價值的量化數據。
- ❌ **難以稽核審計**：生成的摘要缺乏明確的精準出處標籤，無法快速回溯至特定公文或表格。

**`doc-timeline-synthesizer`** 銜接 [docling-skill](https://github.com/realraelrr/docling-skill)（L1 物理轉換層），專注於 **L2 跨文檔語意聚合與時序覆寫**：
1. **時序排序健檢**：自動解析檔名與內文時間戳（民國/西曆），建立時序譜系。
2. **最新拍板覆寫（Latest-Date Overwrite）**：嚴格以最新時間戳記數值覆寫早期預估，鎖定單一真相（Single Source of Truth, SSOT）。
3. **出處嚴格溯源（Citation-Backed）**：每個拍板數字皆標註來源公文檔名與章節表號。
4. **領域驅動隔離（Domain-Driven Segmentation）**：規範「財會、行政、技術」專題目錄分流，杜絕跨領域污染。

---

## 🏛️ 雙層架構圖（Two-Tier Pipeline Architecture）

```text
[ 原始異質文檔 (DOCX / PDF / XLSX / PPTX / 公文簽呈) ]
                          │
                          ▼ (L1: Ingestion Layer)
                 【 docling-skill 】
          • 單文檔物理排版解析 (Docling 核心)
          • CJK 亞洲字距清洗與表格結構還原
          • 產出標準 output/*/source.md + manifest.json
                          │
                          ▼ (L2: Synthesis Layer)
             【 doc-timeline-synthesizer 】
          • 時序預備健檢與指標初篩 (synthesize.py)
          • 行政去雜訊、5D 實體抽取 (Agent 認知層)
          • 時間序新舊衝突覆寫 (Latest-Date Overwrite)
          • 產出各領域《最新拍板總整理.md》
                          │
                          ▼
        [ 下游高精準應用 (NotebookLM / RAG 知識庫 / 首長決策簡報) ]
```

---

## 🚀 快速安裝與環境建置

本專案依賴 [docling-skill](https://github.com/realraelrr/docling-skill) 作為 L1 文檔解析引擎。

### 方式 A：獨立專案安裝（推薦使用 uv）

```bash
# 1. 複製本專案
git clone https://github.com/gemini960114/doc-timeline-synthesizer.git
cd doc-timeline-synthesizer

# 2. 使用 uv 一鍵安裝環境（pyproject.toml 已預設引入 docling-skill）
uv sync

# 或使用標準 pip 安裝
pip install -e .
```

### 方式 B：同時下載兩套 repo 協同開發

若您希望直接檢視或調用 `docling-skill` 的轉換腳本：

```bash
# 建立工作目錄
mkdir -p workspace && cd workspace

# 依序 clone L1 與 L2 套件
git clone https://github.com/realraelrr/docling-skill.git
git clone https://github.com/gemini960114/doc-timeline-synthesizer.git

# 安裝 docling-skill 與相關依賴
cd docling-skill && uv sync && cd ..
cd doc-timeline-synthesizer && uv sync && cd ..
```

### 方式 C：掛載為 AI Agent Skill

本專案根目錄的 `SKILL.md` 符合 Agent 技能規範，可透過軟連結（Symlink）掛載至常用 Agent 工具：

```bash
# Claude Code
ln -sf /path/to/doc-timeline-synthesizer ~/.claude/skills/doc-timeline-synthesizer

# OpenAI Codex / CLI
ln -sf /path/to/doc-timeline-synthesizer ~/.codex/skills/doc-timeline-synthesizer

# Google Antigravity / Gemini CLI
ln -sf /path/to/doc-timeline-synthesizer ~/.gemini/config/skills/doc-timeline-synthesizer
```

---

## 📁 領域驅動目錄架構（Domain-Driven Segmentation）

在實務上，強烈建議**不要將所有文件混在同一目錄**。  
例如：「財務預算表」需要極高的數值精確度，而「行政立法院質詢」包含大量攻防論點與立場答詢。若混在一起合成，容易導致語意稀釋與雜訊互相干擾。

建議採取以下**業務解耦目錄架構**：

```text
my-knowledge-workspace/
├── data/                             # 【原始非結構化文件】按業務領域分類
│   ├── 01_財會預算/                   # 預算概算書、歲出分配表、經費審定書、保留數清單
│   │   ├── 1150601_預算概算提報初稿.docx
│   │   ├── 1150720_跨部會預算協調修正版.docx
│   │   └── 1150828_行政院主計總處歲出核定表.docx
│   │
│   ├── 02_行政管考/                   # 立法院質詢題庫、部會答覆對案、列管檢討簽呈
│   │   ├── 1150715_立法院第1次質詢重點對案.docx
│   │   └── 1150820_行政院列管追蹤進度覆函.docx
│   │
│   └── 03_技術研發/                   # 綱要計畫書、系統架構規格、驗收標準、算力機房指標
│       ├── 1150615_系統架構建置規格草案.pdf
│       └── 1150830_主機建置驗收規範定案.docx
│
├── output/                           # 【docling-skill L1 轉換產物】結構化 source.md
│   ├── 01_財會預算/
│   │   ├── 1150601_預算概算提報初稿/
│   │   │   ├── source.md
│   │   │   └── source.manifest.json
│   │   └── 1150828_行政院主計總處歲出核定表/
│   │       ├── source.md
│   │       └── source.manifest.json
│   ├── 02_行政管考/
│   └── 03_技術研發/
│
└── reports/                          # 【doc-timeline-synthesizer L2 蒸餾成果】
    ├── 01_財會預算_最新拍板總整理.md    # 專屬財會 SSOT
    ├── 02_行政管考_最新拍板總整理.md    # 專屬行政管考 SSOT
    ├── 03_技術研發_最新拍板總整理.md    # 專屬技術規格 SSOT
    └── 全局決策戰略綜合簡報.md        # 金字塔頂層合併（Meta-Synthesis）
```

### 領域隔離的三大優勢：
1. **業務解耦（Decoupling）**：財會專注金額與法定科目；行政專注立委問責與期程列管；技術專注規格與算力數據。
2. **滾動增量更新（Incremental Updating）**：新公文歸檔至指定領域後，僅需重跑該領域的 L1 與 L2，無需全量重跑。
3. **金字塔匯總（Meta-Synthesis）**：當高層首長需要全局簡報時，LLM 僅需綜合 3 份已高度濃縮的《總整理.md》（每份約 2,000 字），數秒內即可產出宏觀決策簡報。

---

## 🛠️ 端到端標準操作流程（Workflow）

### 步驟一：L1 物理轉換（使用 docling-skill）

將原始文件依領域進行批次結構化轉換：

```bash
# 以 01_財會預算 為例
python3 -c "
from pathlib import Path
import subprocess

input_dir = Path('data/01_財會預算')
output_dir = Path('output/01_財會預算')

for file_path in input_dir.glob('*.*'):
    if file_path.suffix.lower() in ['.docx', '.pdf', '.xlsx']:
        cmd = ['docling-skill', 'convert', str(file_path), '--output-dir', str(output_dir / file_path.stem)]
        subprocess.run(cmd, check=True)
"
```

轉換完成後，每個子資料夾會產出清洗完畢的 `source.md` 與標註轉換品質的 `source.manifest.json`。

### 步驟二：L2 時序預備健檢與指標初篩（使用 synthesize.py）

執行時序預備腳本，掃描轉換產物並產出時序清單：

```bash
python3 scripts/synthesize.py \
  --input-dir "./output/01_財會預算" \
  --output-file "output/01_財會預算_inventory.md"
```

**腳本輸出示例**：
```text
📊 掃描完成: 總計 3 份文檔
   已識別時間戳: 3 份
   時間跨度: 1150601 -> 1150828
✔ 成功產出時序預備盤點檔案: output/01_財會預算_inventory.md
```

`inventory.md` 會列出：
- **文檔時序排序表**：按時間由舊至新排列，標註每份文檔的大小、品質狀態。
- **指標初篩片段**：自動抓取含「預算、經費、算力、時程」等關鍵字的重要文句。
- **未定日期文檔（UNDATED）警示**：列出未能自動擷取日期的檔案，提醒手動指定時間權重。

### 步驟三：L2 認知蒸餾與拍板裁決（交由 AI Agent 執行）

在掛載了 `doc-timeline-synthesizer` 的 Agent 環境中（例如 Claude Code、Antigravity），直接向 Agent 下達指令：

> **對話 Prompt 範例**：
> 「請閱讀 `output/01_財會預算_inventory.md` 與 `output/01_財會預算/` 下的文件，嚴格依照 `doc-timeline-synthesizer` 技能規範，執行去雜訊與時序覆寫，產出一份《01_財會預算_最新拍板總整理.md》。」

Agent 將依據 `SKILL.md` 規範，產出符合格式契約的 Single Source of Truth 報告。

---

## 💡 多領域實戰應用範例（Multi-Domain Case Studies）

### 範例一：財會預算領域（數值衝突覆寫實例）

- **輸入文件背景**：
  - `1150601_預算概算提報初稿`：提報「專案 A」115 年度需求為 **12.5 億元**。
  - `1150720_跨部會預算審查會`：刪減非必要項目，修訂為 **10.2 億元**。
  - `1150828_歲出分配核定表`：主計總處法定拍板定案為 **9.8 億元**。

- **L2 合成裁決產出表格**：
  ```markdown
  ## 壹、核心計畫「最新單一真相」數據速查表

  | 計畫名稱 | 全程總經費 | 115年度拍板法定預算 | 初審概算演進 (歷史脈絡) | 最新拍板狀態 | 出處來源 Citation |
  | :--- | :---: | :---: | :--- | :---: | :--- |
  | **專案 A** | 45.0 億元 | **9.8 億元** | 12.5億 (115.06) → 10.2億 (115.07) | ✅ 拍板定案 | `1150828_歲出分配核定表` 表3-1 |
  | **專案 B** | 18.2 億元 | **4.1 億元** | 5.0億 (115.06) → 4.1億 (115.08) | ✅ 拍板定案 | `1150828_歲出分配核定表` 表3-4 |
  ```
  > **核心價值**：被推翻的 12.5 億與 10.2 億僅作為演進軌跡記錄，最新法定定案 9.8 億作為唯一檢索真相，下游 RAG 絕不產生幻覺。

---

### 範例二：行政管考領域（立院質詢與管考爭議演進）

- **輸入文件背景**：
  - `1150715_立法院第1次質詢`：立委質詢專案進度落後 15%，質疑經費支用效益。
  - `1150820_行政院管考檢討`：提報最新改善措施，已透過設備加開班次趕工，實際落後幅度縮小至 2.1%。

- **L2 合成裁決產出結構**：
  ```markdown
  ### 專案進度落後爭議與最新拍板答覆
  - **最新拍板立場（115.08.20 定案）**：
    工程總進度已達 84.3%，落後幅度由 15% 顯著收斂至 2.1%，預計年底前全數追平，無重大違約風險。
    *出處：`1150820_行政院管考檢討` 陸、改善對策*
  - **爭議焦點與演進軌跡（Changelog）**：
    - `115.07.15`：立委質詢主機機房進度落後 15%，要求凍結 10% 預算。
    - `115.08.20`：承辦單位提出機房電力調度與輪班趕工機制，取得管考小組備查。
  ```

---

### 範例三：技術研發領域（規格變更與算力拍板）

- **輸入文件背景**：
  - `1150615_系統架構草案`：原定規劃採購 16 PFLOPS AI 算力主機，PUE 指標設定為 1.35。
  - `1150830_主機採購規範定案`：配合先進製程伺服器，拍板調升算力至 **32 PFLOPS**，PUE 嚴格限制為 **1.25**。

- **L2 合成裁決產出速查表**：
  ```markdown
  | 系統項目 | 初期規劃 (115.06) | 最新拍板定案規格 (115.08) | 技術變更理由 | 出處來源 Citation |
  | :--- | :--- | :--- | :--- | :--- |
  | **AI 算力總量** | 16 PFLOPS | **32 PFLOPS** | 採用新世代 GPU 晶片模組 | `1150830_主機採購規範定案` 參、主機規格 |
  | **機房能效 (PUE)** | ≤ 1.35 | **≤ 1.25** | 導入水冷式散熱架構 | `1150830_主機採購規範定案` 肆、機電標準 |
  ```

---

### 範例四：金字塔戰略綜整（Meta-Synthesis）

當主管或決策層需要跨領域的宏觀報告時：

```text
  【財會總整理.md】     【行政管考總整理.md】     【技術研發總整理.md】
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │ (LLM 頂層跨域綜合)
                               ▼
                【 全局決策戰略綜合簡報.md 】
         (1. 核心預算與財務缺口盤點 -> 2. 技術規格與算力產能 -> 3. 立院管考攻防重點)
```

- **優點**：LLM 處理的文本已全數經過 L2 去雜訊與覆寫，總上下文僅約 6,000 字，合成只需 10 秒，且精準度達到 100%。

---

## 🔒 資安與機敏資料防護機制

在處理公部門公文、企業未公開財報或專案預算時，**資料隱私與合規安全**至關重要：

1. **本機端完全運作（Local-First Execution）**：
   - 腳本 `synthesize.py` 與 `docling-skill` 解析完全於本機執行，無需將文檔上傳至外部第三方處理平台。
2. **嚴格的 `.gitignore` 白名單防護**：
   - 倉庫內建完整忽略機制，包含 `data/`、`output/`、`*.docx`、`*.pdf`、`*.xlsx`、`*總整理*.md`、`process.md` 等工作文件。
   - 任何涉及內部人員真實姓名、機密預算數字之實體文件均受版本控制隔離，保證不會意外推送至公開 GitHub 倉庫。
3. **安全提交檢查清單**：
   ```bash
   # 檢查是否有未受忽略之資料檔案
   git status --ignored

   # 確保 tracked 檔案中無機敏關鍵字
   git grep -i "機密"
   ```

---

## 📄 授權條款與致謝

- **授權條款**：本專案採用 [MIT License](LICENSE) 授權開源。
- **致謝**：
  - 感謝 [IBM Docling](https://github.com/docling-project/docling) 提供世界級的文檔版面分析與 OCR 能力。
  - 感謝 [realraelrr/docling-skill](https://github.com/realraelrr/docling-skill) 提供專為 Agent 設計的 CJK 清洗與高品質轉換層。
