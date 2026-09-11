# 合成端到端範例

繁體中文 | [English](EXAMPLE.md)

本文件只使用虛構檔名與數值，不包含研究語料內容。

## 1. 準備隔離的本機資料

    mkdir -p data/example_domain
    mkdir -p output/example_domain
    mkdir -p reports

範例文件：

    data/example_domain/
      2025-01-10_initial_plan.docx
      2025-03-15_approved_revision.pdf
      2025-04-02_status_note.xlsx

上述資料夾已由 Git 排除，必須保留在本機。

## 2. 執行 L1 轉換

使用 docling-skill 為每份來源文件建立獨立輸出資料夾。每個資料夾至少應有 source.md，並視情況包含 source.manifest.json 與 source.evidence.json。

## 3. 檢查圖片

    uv run python scripts/scan_image_placeholders.py       --input-dir output/example_domain

若圖片包含決策相關證據，將說明寫入 source.images.md 並對應原始 placeholder。若只是標誌或裝飾圖片，應建立附理由的略過紀錄，不可默默忽略。

## 4. 建立時序盤點

    uv run python scripts/synthesize.py       --input-dir output/example_domain       --output-file output/example_domain_inventory.md

盤點檔只是診斷索引，不是最終證據。Agent 仍須完整閱讀所有相關來源。

## 5. 執行範圍感知蒸餾

建議 prompt：

    閱讀 output/example_domain_inventory.md，以及
    output/example_domain 下所有 source.md、manifest 與相關圖片 sidecar。
    依 SKILL.md 建立附引用的總整理。只有在實體、屬性、期間、範圍、
    單位與語意一致時才比較候選值；綜合時間、出處、文件狀態與簽核
    狀態判定權威性。無法解決的衝突必須保留。輸出至
    reports/example_domain_summary.md。

合成的跨文件衝突：

- 2025-01-10 草稿記載原規劃容量為 100 單位。
- 2025-03-15 核定修正版對相同地點、期間與定義記載 112 單位。
- 2025-04-02 狀態報告記載 118 單位，但多包含另一個地點。

第三個值雖然更新，但範圍不同。合理輸出可在原範圍採用 112，另行揭露較大範圍的 118；不可只因日期較新便直接覆寫。

合成的文件內衝突：

- 敘述文字寫 40 單位。
- 正式核定欄位寫 4 單位。
- 範本比對顯示敘述文字由另一份表單沿用。

本案例可依文件狀態、欄位用途及佐證選擇結構化值，但不能把這個判斷升格為「結構化資料永遠優先」。

## 6. 執行 L3 審核

另開新的 agent context，只提供成品報告與原始來源路徑，不提供產出者的對話歷史或推理軌跡。

建議 prompt：

    使用 doc-timeline-auditor/SKILL.md 審核
    reports/example_domain_summary.md，來源為 output/example_domain。
    逐一解析引用、檢查來源風險與跨版本拼接、抽查遺漏內容、重算
    衍生數值並確認統計範圍。以 PASS、PASS WITH CAVEATS 或 FAIL
    回報，每項發現都要附證據。

## 7. 建立 RAG 輸入

    uv run python scripts/build_rag_bundle.py       --input-dir output/example_domain

存在圖片 sidecar 時，應索引 source.rag.md，而非直接索引 source.md。

## 8. 公開前檢查

- 確認來源持有者允許公開；
- 移除識別資訊與受限內容；
- 由人工核對重要數值；
- 檢查實際 Git staged files；
- 原始文件與產出報告不得放入公開 repo。
