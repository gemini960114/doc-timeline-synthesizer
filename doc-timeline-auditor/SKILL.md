---
name: doc-timeline-auditor
description: Use after doc-timeline-synthesizer produces a 《總整理.md》or《全局決策戰略綜合簡報.md》, to run an independent adversarial audit against the original source.md/manifest.json corpus before the report is treated as decision-ready — verifies every citation actually resolves, catches cross-timestamp unit-splicing, and surfaces any high-risk docling-skill sources the synthesis step didn't disclose.
---

# doc-timeline-auditor

`doc-timeline-auditor` 是 `doc-timeline-synthesizer`（L2 Synthesis Layer）的**獨立第三層審核（L3 Audit Layer）**。
它不產生新的總整理內容，只對**已產出**的《總整理.md》或《全局決策戰略綜合簡報.md》做逆向查核，判定它是否真的可以交給首長／立法院當作決策依據。

---

## 為什麼需要獨立於蒸餾 Agent 之外

`doc-timeline-synthesizer` 步驟四已內建「抽樣回溯驗證」，但那是**同一個 Agent 在同一個對話 context 裡自我檢查**——它傾向於驗證自己剛下的結論，而不是真的用懷疑角度重查。實務上已經證實這類自我審查會漏掉：
- 把舊時間戳文件的某個計量單位，和新時間戳文件的另一個單位拼接成同一句主張（新舊數值混拼）。
- 把數字的出處標成錯誤的檔名（引用錯置）——尤其是跨領域彙整時，數字其實來自另一個領域的文件。
- 直接引用被 `docling-skill` 自己標記為 `agent_ready: false` / `risk_level: high` 的來源，卻未在報告中揭露風險。

這些錯誤的共同特徵是：**產生錯誤的那個推理路徑，也正是自我檢查時會被重複套用的路徑**。因此審核必須由一個**沒有讀過蒸餾過程、只看得到「成品報告」與「原始語料庫」的全新 Agent / Session** 來執行，才能真正扮演對抗性的第二視角。

> [!IMPORTANT]
> **執行方式**：務必以全新的 Agent 對話（例如另開一個 Claude Code session、或用 Agent 工具起一個全新 subagent）執行本技能，不可與產出《總整理.md》的同一個對話接續進行。審核者的 prompt 只應包含「待審報告路徑」與「原始語料庫路徑」，不應附上蒸餾 Agent 的推理紀錄或對話摘要。

---

## 稽核輸入（Audit Inputs）

1. **待審報告**：一份或多份《總整理.md》，或金字塔頂層的《全局決策戰略綜合簡報.md》。
2. **原始語料庫**：報告所屬領域 `output/<domain>/*/source.md`、`source.manifest.json`、`source.evidence.json` 全集——**不是** `chronological_inventory.md` 的截斷片段。

---

## 五大稽核維度（5 Audit Dimensions）

### 1. 引用可解性（Citation Resolvability）
對報告中**每一個** Citation 標籤，實際回到其宣稱的 `source.md` 用文字檢索確認：
- 該數字（含單位）真的存在於該檔案中。
- 若檢索不到，往其他領域的 `source.md` 反查，確認是否為「引用錯置」（數字是真的，但出處標錯檔名）。

### 2. 來源風險揭露（Source Risk Disclosure）
對每一個被引用的來源檔案，讀取其 `source.manifest.json`：
- 若 `decision.agent_ready: false` 或 `decision.risk_level: "high"`，檢查報告的 Citation 欄位是否已標註「⚠ 來源標記高風險」。未標註者列為缺失。
- 若 `risk_level: "medium"` 且 `warnings` 含 `replacement_characters`，快速確認引用段落附近沒有殘留 `U+FFFD`／`�`。

### 3. 跨時間戳拼接檢測（Anti-Splicing Check）
找出報告中「多個計量單位共同描述同一指標」的敘述（例如「MW」與「PF／PB」成組出現、「千元」與「百分比」成組出現），逐一確認每個單位是否來自**同一份、同一時間戳**的來源文件。凡混用不同時間戳文件的不同單位者，列為缺失並指出正確的最新單一來源。

### 4. 覆蓋度抽查（Coverage Sampling）
針對報告引用的**大型**來源文件（例如字元數超過 5 萬字的綱要計畫書、歲出概況表），隨機抽查 2-3 個報告完全沒提到的段落或表格列，確認：
- 是否存在與報告已收錄項目同等重要、但被漏掉的指標修正／爭議項目（例如同一份 A009 修正表裡的其他關鍵成果變更）。
- 藉此推估報告的實際覆蓋率，而非僅信任蒸餾 Agent 自陳「重點已涵蓋」。

### 5. 數值重算驗證（Arithmetic Re-derivation）
對報告中出現的加總、佔比、成長率等衍生計算（例如「五大計畫合計 348.63 億」「資本門佔比 88.87%」），獨立重新算一次，確認與報告數字一致。

---

## 交付成果規格（Audit Output Contract）

產出《審核意見.md》，結構如下：

1. **總評判定**：`PASS`（可直接交付）／`PASS WITH CAVEATS`（可交付但需附帶揭露事項）／`FAIL`（不得交付，需退回蒸餾階段重做）。
2. **逐項稽核發現**，依嚴重度排序，每項包含：
   - 位置（檔名＋章節／表格）
   - 問題描述（違反上述哪一項稽核維度）
   - 失效情境（若不修正，下游會被誤導成什麼結論）
   - 建議修正
3. **已核實通過清單**：至少列出隨機抽查後確認無誤的項目，避免報告讀起來像「只挑錯」，也讓蒸餾 Agent 知道哪些部分做對了。

> [!NOTE]
> 審核者**不修改**原報告內容，只產出審核意見；是否採納、如何修正，交回 `doc-timeline-synthesizer` 的蒸餾流程或人類決定。判定為 `FAIL` 的報告，在對外或送審前不得標示為「已完成」。
