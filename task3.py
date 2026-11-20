import pandas as pd
import plotly.express as px

# 1. 定義欄位名稱
cols = ['time', 'host', 'disk', 'Type', 'Offset', 'Size', 'resp_ms']

# 2. 讀取資料檔案（如果是 Excel 檔用 read_excel，如果是 CSV 用 read_csv）
df = pd.read_excel(r"檔案路徑名稱", header=None, names=cols)

# ==========================================
# Task 3: 回應時間調查 (Response-time Investigation)
# ==========================================
# 計算讀寫延遲的統計量（中位數、p95、p99、平均值）
latency_summary = df.groupby('Type')['resp_ms'].agg(
    median='median',
    p95=lambda x: x.quantile(0.95),
    p99=lambda x: x.quantile(0.99),
    mean='mean',
    max='max'
).reset_index()

print("=== Task 3: 延遲統計摘要 ===")
print(latency_summary)

# 產出圖表 A：讀寫延遲分佈盒鬚圖
fig_box = px.box(df, x='Type', y='resp_ms', log_y=True, 
                 title="Task 3: Read vs Write Response Time Distribution")
fig_box.show()

# 產出圖表 B：請求大小 vs. 回應時間散佈圖
fig_scatter = px.scatter(df.sample(min(5000, len(df))), x='Size', y='resp_ms', color='Type',
                         title="Task 3: Request Size vs Response Time",
                         labels={'Size': 'Request Size (Bytes)', 'resp_ms': 'Response Time (ms)'})
fig_scatter.show()