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

若圖片包含決策相關證據，將說明寫入 source.images.md 並對應原始 placeholder。若經判定不具決策實質內容（例如純商標或活動照片），應建立附理由的略過紀錄，不可默默忽略。

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

## 8. 建置分層雙庫 RAG 檢索（合成範例）

為平衡細部公文脈絡與權威仲裁事實，建議在下游建立雙集合：

1. **`raw_corpus` 集合**：索引 `output/` 下的分塊 `source.rag.md`。
2. **`ssot_reports` 集合**：索引 `reports/` 下的分塊領域總整理。

查詢時實施分層仲裁：
- 同時檢索兩庫（例如分別取出 `raw_corpus` 前 5 名與 `ssot_reports` 前 5 名分塊）。
- 使用具備優先權仲裁的 System Prompt：
  > 「你獲取了兩組知識庫：[SSOT_REPORTS]（經稽核之領域權威總整理）與
  > [RAW_CORPUS]（詳細歷史公文片段）。若兩者在數值、事實或時序上產生衝突，
  > 請一律以 [SSOT_REPORTS] 之裁定值為最終權威答案，並以 [RAW_CORPUS]
  > 補充歷史演進與脈絡說明。」

此設計可徹底防止原始公文中已被覆蓋的早期草案干擾生成，同時完整保留歷史推演細節。

## 9. 公開前檢查

- 確認來源持有者允許公開；
- 移除識別資訊與受限內容；
- 由人工核對重要數值；
- 檢查實際 Git staged files；
- 原始文件、評測資料集、向量資料庫與產出報告不得放入公開 repo。
