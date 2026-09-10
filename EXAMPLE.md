# 專案實戰 SOP：doc-timeline-synthesizer 從零到產出全流程手冊 (process.md)

> **版本**：v1.1.0（新增階段八：L3 獨立審核 doc-timeline-auditor）  
> **適用環境**：Linux / macOS（支援 Google Antigravity, Claude Code, OpenAI Codex, 多 Agent 框架）  
> **核心定位**：跨文檔多版次時序聚合、新舊衝突裁決與單一真相（SSOT）提煉標準作業流程。

---

## 📑 目錄
1. [系統三層架構設計觀念](#1-系統三層架構設計觀念)
2. [階段零：全新機器前置準備（Python 3.10+ 與 uv）](#2-階段零全新機器前置準備python-310-與-uv)
3. [階段一：從 GitHub Clone 核心套件與環境初始化](#3-階段一從-github-clone-核心套件與環境初始化)
4. [階段二：建立新業務專案目錄與資安隔離](#4-階段二建立新業務專案目錄與資安隔離)
5. [階段三：專案層級（Project-Level）Skill 掛載（含 .agents 規範）](#5-階段三專案層級project-levelskill-掛載含-agents-規範)
6. [階段四：文件歸檔與時間戳命名規範](#6-階段四文件歸檔與時間戳命名規範)
7. [階段五：執行 L1 物理轉換（docling-skill）](#7-階段五執行-l1-物理轉換docling-skill)
8. [階段六：執行 L2 時序預備健檢與指標初篩（synthesize.py）](#8-階段六執行-l2-時序預備健檢與指標初篩synthesizepy)
9. [階段七：交由 AI Agent 執行語意蒸餾與裁決產出](#9-階段七交由-ai-agent-執行語意蒸餾與裁決產出)
10. [階段八：交付獨立審核（L3 Audit，換一個全新 Agent）](#10-階段八交付獨立審核l3-audit換一個全新-agent)
11. [階段九：常見錯誤排查與資安檢查表](#11-階段九常見錯誤排查與資安檢查表)

---

## 1. 系統三層架構設計觀念

在公部門、科技專案與大型組織中，文檔（Word、PDF、公文、題庫、預算書）會歷經數個月的多輪審查。  
如果將未經時序整理的檔案直接丟給一般 RAG，會導致**「6月提報預算」與「8月拍板定案」同時被撈出，造成 AI 嚴重幻覺**。

本架構切分為三層：
* **L1 Ingestion Layer（物理轉換層 - `docling-skill`）**：
  * 負責複雜版面解析、表格還原、CJK 亞洲字距去空格修復。
  * 產出標準且格式統一的 `output/*/source.md` 與品質診斷 `source.manifest.json`（含 `agent_ready`／`risk_level` 分級）。
* **L2 Synthesis Layer（認知蒸餾層 - `doc-timeline-synthesizer`）**：
  * 負責**跨文檔時序排序**、**樣板行政雜訊過濾**、**5D 實體抽取**。
  * 核心法則：**「後出文檔數值直接覆寫舊數值（Latest-Date Overwrite）」**，並附帶精準出處標註（Citation）。
* **L3 Audit Layer（獨立審核層 - `doc-timeline-auditor`）**：
  * 由**另一個全新 Agent／Session** 執行，不接觸 L2 的推理過程，只拿「成品報告＋原始語料庫」逆向核對。
  * 專門攔截 L2 自我檢查容易漏掉的錯誤：新舊數值拼接、引用出處錯置、高風險來源未揭露。

```text
[ 原始各類公文/報告 ]
        │
        ▼ (L1: Ingestion)
 【 docling-skill 】 ── 單文檔排版解析、清洗 CJK 字距，產出 output/*/source.md
        │
        ▼ (L2: Synthesis)
 【 doc-timeline-synthesizer 】 ── 跨文檔時序排序、新舊數值覆寫，產出《最新拍板總整理.md》
        │
        ▼ (L3: Audit，換一個全新 Agent／Session)
 【 doc-timeline-auditor 】 ── 逆向核對 Citation、來源風險、跨時間戳拼接，產出《審核意見.md》
        │
        ▼（僅限 PASS / PASS WITH CAVEATS）
 [ 下游精準應用 ] ── NotebookLM / 高精準 RAG / 首長決策簡報
```

> 內部草稿或低風險用途可以只做到 L2；任何要送交決策層、立法院或對外公開的報告，強烈建議一定要跑 L3。

---

## 2. 階段零：全新機器前置準備（Python 3.10+ 與 uv）

在全新的 Linux / Ubuntu 機器上，依序安裝必要基礎工具：

```bash
# 1. 更新套件清單並安裝基礎開發工具
sudo apt update && sudo apt install -y git python3 python3-pip python3-venv curl

# 2. 安裝極速 Python 套件管理器 uv（下載與解析速度較 pip 快 10~50 倍）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 讓 uv 指令立即生效
source ~/.bashrc  # 若使用 zsh 請執行 source ~/.zshrc
uv --version
```

---

## 3. 階段一：從 GitHub Clone 核心套件與環境初始化

將兩套開源核心套件下載至統一代碼目錄（例如 `~/github`）：

```bash
# 1. 建立統一代碼目錄
mkdir -p ~/github && cd ~/github

# 2. Clone L1 與 L2 倉庫
git clone https://github.com/realraelrr/docling-skill.git
git clone https://github.com/gemini960114/doc-timeline-synthesizer.git

# 3. 進入 doc-timeline-synthesizer，由 uv 自動建置虛擬環境並安裝所有依賴
cd ~/github/doc-timeline-synthesizer
uv sync
```

> **驗證依賴安裝**：
> 執行 `uv run python3 -c "import docling; print('Docling ready!')"`，若印出 `Docling ready!` 即代表底層解析引擎與依賴皆已正確安裝。

---

## 4. 階段二：建立新業務專案目錄與資安隔離

**核心原則**：業務專案與工具倉庫分開，維持專案獨立與資安隔離。

```bash
# 1. 建立並進入您的全新業務專案（名稱可自訂，如 my-project）
mkdir -p ~/github/my-project && cd ~/github/my-project

# 2. 建立領域驅動目錄（Domain-Driven Directory）
mkdir -p data/01_財會預算
mkdir -p data/02_行政管考
mkdir -p data/03_技術研發
mkdir -p output reports

# 3. 初始化 Git 並套用防洩漏 .gitignore（防止機敏公文與數據被誤推至遠端）
git init
cp ~/github/doc-timeline-synthesizer/.gitignore .
git add .gitignore
git commit -m "chore: initialize project with domain structure and secure gitignore"
```

---

## 5. 階段三：專案層級（Project-Level）Skill 掛載（含 .agents 規範）

### 為什麼採用專案層級（Project-Level）而非全域（Global）？
* **避免全域環境污染**：不同專案可能有不同的 Skill 版本需求，專案級只在「當前資料夾」生效。
* **支援多 Agent 規範**：Google Antigravity 優先讀取專案根目錄下的 `.agents/`；Claude Code 讀取 `.claude/`；Codex 讀取 `.codex/`。

### ⚠️ 常見錯誤警示：為什麼 `ln` 會報錯？
若直接執行：
```bash
ln -sfn ~/github/doc-timeline-synthesizer .agents/skills/doc-timeline-synthesizer
# ❌ 報錯：ln: failed to create symbolic link '.agents/skills/...': No such file or directory
```
**原因**：Linux 建立軟連結時，目標路徑的父目錄（`.agents/skills/`）必須先存在！

### ✅ 正確操作標準步驟（包含 mkdir -p）：

```bash
# 確保在您的當前專案目錄
cd ~/github/my-project

# 步驟 1：先行建立所有 Agent 所需的 skills 父目錄
mkdir -p .agents/skills .claude/skills .codex/skills .gemini/skills

# 步驟 2：執行軟連結 doc-timeline-synthesizer（L2 蒸餾，此時父目錄已齊全，100% 成功）
ln -sfn ~/github/doc-timeline-synthesizer .agents/skills/doc-timeline-synthesizer
ln -sfn ~/github/doc-timeline-synthesizer .claude/skills/doc-timeline-synthesizer
ln -sfn ~/github/doc-timeline-synthesizer .codex/skills/doc-timeline-synthesizer
ln -sfn ~/github/doc-timeline-synthesizer .gemini/skills/doc-timeline-synthesizer

# 步驟 3：另外軟連結 doc-timeline-auditor（L3 獨立審核）
ln -sfn ~/github/doc-timeline-synthesizer/doc-timeline-auditor .agents/skills/doc-timeline-auditor
ln -sfn ~/github/doc-timeline-synthesizer/doc-timeline-auditor .claude/skills/doc-timeline-auditor
ln -sfn ~/github/doc-timeline-synthesizer/doc-timeline-auditor .codex/skills/doc-timeline-auditor
ln -sfn ~/github/doc-timeline-synthesizer/doc-timeline-auditor .gemini/skills/doc-timeline-auditor
```

> **兩個技能都要掛載，但執行時分開用**：`doc-timeline-synthesizer` 在階段七的對話裡呼叫；`doc-timeline-auditor` 要留到階段八，在**另一個全新對話**裡呼叫，不能接續階段七的 context。

### 驗證掛載：
```bash
ls -la .agents/skills/
# 預期輸出：
#   doc-timeline-synthesizer -> /home/ubuntu/github/doc-timeline-synthesizer
#   doc-timeline-auditor -> /home/ubuntu/github/doc-timeline-synthesizer/doc-timeline-auditor
```

---

## 6. 階段四：文件歸檔與時間戳命名規範

### 領域資料夾分流原則：
| 目錄路徑 | 適用收納文檔類型 | 核心關注指標 |
| :--- | :--- | :--- |
| `data/01_財會預算/` | 概算提報表、歲出分配核定表、經費審查會紀錄、保留數清單 | 全程預算、法定預算、資本門/經常門 |
| `data/02_行政管考/` | 立法院質詢題庫、部會答覆對案、管考改善簽呈、期程檢討 | 爭議焦點、質詢責任、行政改善進度 |
| `data/03_技術研發/` | 綱要計畫書、核心架構規格書、算力機房標準、驗收規範 | PFLOPS、MW、PUE、時程里程碑 |

### 命名最佳實踐（提高時序辨識率至 100%）：
建議在檔名開頭加上**民國 7 碼**或**西元 8 碼**時間戳：
* 推薦：`1150828_行政院主計總處歲出核定表.docx`
* 推薦：`2026-09-04_立法院質詢對案.docx`
* 推薦：`1150615_系統架構規格需求草案.pdf`

---

## 7. 階段五：執行 L1 物理轉換（docling-skill）

啟用 `doc-timeline-synthesizer` 虛擬環境，將指定領域的文檔批次轉為標準 `source.md`：

```bash
cd ~/github/my-project

# 啟動環境
source ~/github/doc-timeline-synthesizer/.venv/bin/activate

# 以「01_財會預算」為例執行批次轉換
python3 -c "
from pathlib import Path
import subprocess

domain = '01_財會預算'
input_dir = Path(f'data/{domain}')
output_dir = Path(f'output/{domain}')

for file_path in input_dir.glob('*.*'):
    if file_path.suffix.lower() in ['.docx', '.pdf', '.xlsx']:
        print(f'正在轉換: {file_path.name}')
        cmd = ['docling-skill', 'convert', str(file_path), '--output-dir', str(output_dir / file_path.stem)]
        subprocess.run(cmd, check=True)
print('✔ 批次轉換完成！')
"
```

**產物結構**：
```text
output/01_財會預算/
├── 1150601_預算概算提報初稿/
│   ├── source.md             <--- 清洗完成之結構化 Markdown
│   └── source.manifest.json  <--- 包含字數、OCR 決策與品質指標
└── 1150828_行政院主計總處歲出核定表/
    ├── source.md
    └── source.manifest.json
```

---

## 8. 階段六：執行 L2 時序預備健檢與指標初篩（synthesize.py）

使用內建健檢腳本對 output 目錄執行時序譜系掃描：

```bash
python3 ~/github/doc-timeline-synthesizer/scripts/synthesize.py \
  --input-dir output/01_財會預算 \
  --output-file output/01_財會預算_inventory.md
```

### 終端機健檢輸出解析：
```text
📊 掃描完成: 總計 3 份文檔
   已識別時間戳: 3 份
   時間跨度: 1150601 -> 1150828
✔ 成功產出時序預備盤點檔案: output/01_財會預算_inventory.md
```
* 如果有檔案未能辨識出日期，終端機會出現 `⚠️ 警告: 發現 X 份未識別明確時間戳的文件 (UNDATED)`，提醒您手動核對時間序。
* `inventory.md` 內會依時間**由舊到新**嚴密排序，並列出經費、算力、時程之初篩片段。

---

## 9. 階段七：交由 AI Agent 執行語意蒸餾與裁決產出

由於當前專案已具備 `.agents/skills/doc-timeline-synthesizer`，AI Agent 會自動載入該技能的行為準則。

### Prompt 範本 A：單領域單一真相蒸餾（以財會預算為例）

在對話框中直接發送：

```text
請依據已載入的 doc-timeline-synthesizer 規範，閱讀 output/01_財會預算_inventory.md 與 output/01_財會預算/ 下的所有 source.md 文件，為我執行跨文檔去雜訊與時序覆寫：

1. 嚴格遵守「後發布時間點數值直接覆寫舊數值」法則，將最新拍板定案確立為唯一主數據。
2. 建立「壹、核心計畫最新單一真相數據速查表」，欄位包含：計畫名稱、全程經費、115年度拍板預算、初審概算演進歷程、拍板狀態、出處來源 Citation。
3. 每個關鍵數字必須明確標註出處檔名與章節表號（例如：`1150828_歲出核定表` 表3-1）。
4. 忽略公文收發文號、會簽代碼、樣板問候語。
5. 產出報告儲存至：reports/01_財會預算_最新拍板總整理.md
```

---

### Prompt 範本 B：金字塔頂層戰略匯總（Meta-Synthesis）

當各領域皆已產出總整理後，下達以下 Prompt 產出宏觀決策簡報：

```text
我已完成各領域的最新拍板總整理：
- reports/01_財會預算_最新拍板總整理.md
- reports/02_行政管考_最新拍板總整理.md
- reports/03_技術研發_最新拍板總整理.md

請進行金字塔頂層跨域綜合，產出一份給高層決策使用的《reports/全局決策戰略綜合簡報.md》：
1. 聚焦全局重點預算規模與資金缺口。
2. 匯總關鍵技術指標（算力建置、PUE 規格）與預計完工里程碑。
3. 列管立法院攻防焦點與最新官方答覆對策。
```

---

## 10. 階段八：交付獨立審核（L3 Audit，換一個全新 Agent）

階段七產出的《總整理.md》**只是初稿**，真正決定它能不能交給首長或立法院的，是這一步的獨立審核。

### ⚠️ 關鍵前提：一定要換一個新對話
如果你在同一個對話視窗裡接著問「幫我審查一下剛剛的報告」，Agent 會**傾向於驗證自己剛剛下的結論**，等於自己審自己的考卷。正確做法：
1. 開一個全新的 Claude Code / Antigravity / Codex 對話（或用 Agent 工具另起一個 subagent）。
2. 確認這個新對話已經掛載了 `doc-timeline-auditor`（見階段三）。
3. 只給它「待審報告路徑」與「原始語料庫路徑」，**不要**貼上階段七的對話紀錄或推理過程。

### Prompt 範本 C：獨立審核已產出的總整理

在**全新對話**中發送：

```text
請依照已載入的 doc-timeline-auditor 規範，審核 reports/01_財會預算_最新拍板總整理.md。

原始語料庫在 output/01_財會預算/ 下（每份文件皆有 source.md、source.manifest.json、source.evidence.json）。

請不要假設報告內容正確，逐一執行五大稽核維度：
1. 回溯報告中每一個 Citation 到來源 source.md，確認數字真的存在該檔案中。
2. 核對每個被引用來源的 source.manifest.json，若 agent_ready 為 false 或 risk_level 為 high，確認報告是否已標註風險。
3. 找出報告中「多個計量單位共同出現」的敘述（如 MW 與 PF/PB 成組出現），確認是否來自同一份、同一時間戳文件。
4. 對引用的大型來源文件（字元數 > 5 萬），隨機抽查 2-3 段報告未提及的內容，評估是否有漏抓的重要修正項目。
5. 獨立重算報告中的加總、佔比、成長率，確認與報告數字一致。

最後產出 reports/01_財會預算_審核意見.md，總評為 PASS / PASS WITH CAVEATS / FAIL 三選一，並列出逐項稽核發現與已核實通過清單。
```

### 判讀結果：
- **`PASS`**：可直接交付下游使用。
- **`PASS WITH CAVEATS`**：可交付，但需在報告中補上審核意見指出的揭露事項（例如標註某數字來自高風險來源）。
- **`FAIL`**：退回階段七，依審核意見修正後重新蒸餾，再送一次階段八，直到不再是 `FAIL`。

> 金字塔頂層的《全局決策戰略綜合簡報.md》也要比照辦理——用另一個全新對話對它跑一次 `doc-timeline-auditor`，因為它常會原樣複製各領域總整理裡的錯誤，審核時要特別檢查錯誤是否被放大擴散。

---

## 11. 階段九：常見錯誤排查與資安檢查表

### 常見問題速查：
1. **問題：`ln: failed to create symbolic link ... No such file or directory`**
   * **原因**：父資料夾尚未建立。
   * **解法**：執行 `mkdir -p .agents/skills .claude/skills .codex/skills .gemini/skills` 後再建立軟連結。
2. **問題：`docling-skill: command not found`**
   * **原因**：尚未啟用虛擬環境。
   * **解法**：執行 `source ~/github/doc-timeline-synthesizer/.venv/bin/activate`。
3. **問題：時序清單出現 `999999_UNDATED`**
   * **原因**：檔名與開頭內文缺少 7 碼民國或 8 碼西曆日期。
   * **解法**：建議手動修改檔名（如加上 `1150820_`）後重新執行 `synthesize.py`。

### 資安防洩漏檢查清單（提交 Git 前必做）：
在專案目錄執行以下兩道指令，確認機敏資料未被 Git 追蹤：

```bash
# 1. 檢查是否有未被忽略的資料文件（應只看到 .gitignore 或腳本）
git status --ignored

# 2. 搜尋是否包含機敏人名或單位名稱
git grep -i -E "機密|身分證|未公開"
```
若工作區乾淨且無任何非結構化文件被 stage，即可安全進行版本控制。
