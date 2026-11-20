[README.md](https://github.com/user-attachments/files/35160931/README.md)

# 磁碟 I/O 分析：MSR Cambridge Block I/O Traces

> 【待填】課程名稱、組員、指導老師

## 專案簡介

本專案分析 MSR Cambridge Block I/O Traces 的磁碟 I/O 行為，包含讀寫比例、請求大小、回應時間與存取局部性等面向。分析結果以互動式網站呈現（GitHub Pages）。

**研究問題**：【待填，第 1 週定義後補上】

## 資料集

- **名稱**：MSR Cambridge Block I/O Traces
- **來源**：SNIA IOTTA Repository，https://iotta.snia.org/traces/block-io/388
- **內容**：依 README，發行包含 36 個 I/O trace，來自 13 台伺服器的 36 個磁碟區；每個檔案命名為 `<hostname>_<disknumber>.csv.gz`
- **本專案使用的檔案**：【待填】目前已下載 Traces 1（`msr-cambridge1.tar`，3.06 GB），內含 hm、mds、prn、proj、prxy 五台伺服器共 13 個磁碟區；Traces 2 【待確認／待下載】
- **引用文獻**：Narayanan, D., Donnelly, A., Rowstron, A. *Write Off-Loading: Practical Power Management for Enterprise Storage.* Proc. 6th USENIX Conference on File and Storage Technologies (FAST '08).

### 欄位與單位

檔案為 gzip 壓縮的 CSV，**沒有標題列**，欄位順序如下（依據資料集 README.txt）：

| 欄位 | 說明 | 原始單位 | 分析時轉換成 |
|---|---|---|---|
| Timestamp | I/O 發出的時間 | Windows filetime（1 單位 = 100 ns，從 1601/1/1 起算） | datetime（UTC）或距起點的秒數 |
| Hostname | 主機名稱 | 文字 | — |
| DiskNumber | 邏輯磁碟編號 | 整數 | — |
| Type | Read 或 Write | 文字 | — |
| Offset | 從邏輯磁碟起點算起的起始位置 | bytes | GB |
| Size | 傳輸大小 | bytes | KB |
| ResponseTime | I/O 完成所花時間 | Windows filetime 單位（100 ns） | ms |

說明：資料集 README 只寫 Timestamp 與 ResponseTime 為 "Windows filetime"；「1 單位 = 100 ns」是 Windows FILETIME 的規格。完整對照表見 `docs/MSR_欄位單位對照表.xlsx`。

換算公式：

```python
FILETIME_EPOCH = 116444736000000000                 # 1601-01-01 到 1970-01-01，單位 100 ns
df["time"]    = pd.to_datetime((df["Timestamp"] - FILETIME_EPOCH) // 10, unit="us")
df["size_kb"] = df["Size"] / 1024
df["resp_ms"] = df["ResponseTime"] / 10_000
```

磁碟編號備註：disk 0 通常是系統碟，但 `src1` 例外，其系統碟為 disk 2。

## 專案結構

```
.
├── README.md
├── .gitignore
├── docs/
│   └── MSR_欄位單位對照表.xlsx
├── scripts/
│   └── preprocess.py        # 原始 csv.gz → parquet
├── notebooks/               # 【待補】分析與畫圖
├── data/
│   ├── raw/                 # 原始 trace（不放進 git）
│   └── processed/           # 處理後的檔案（不放進 git，或只放小檔）
└── site/                    # 【待補】GitHub Pages 網站
```

## 環境

- Python 3.11（Windows 以 `py` 執行）
- 套件：pandas、pyarrow、plotly

```
py -m pip install pandas pyarrow plotly
```

## 如何重現

1. 到 SNIA 頁面下載 MSR Cambridge Traces（需開啟 cookies），解開後把 `.csv.gz` 放進 `data/raw/`。**原始資料不會放進此 repo。**
2. 前處理：
   ```
   py scripts/preprocess.py
   ```
   【待補】說明輸入路徑、輸出路徑，以及每個檔案的筆數。
3. 分析與畫圖：依序執行 `notebooks/` 內的 notebook 【待補檔名與順序】。
4. 圖表輸出到 `site/` 【待補】。

## 前處理紀錄

【待補，第 2 週完成後填寫，網站 Dataset 章節會用到】

- 欄位命名：統一使用上表的 7 個欄位名稱
- 單位換算：見上表
- 資料品質檢查：缺值、重複列、時間戳是否遞增、Size 與回應時間異常值 【待填結果】
- 子集或抽樣：【待填範圍與理由】
- 輸出格式：parquet

## 網站

【待補】GitHub Pages 網址、互動元素說明。
