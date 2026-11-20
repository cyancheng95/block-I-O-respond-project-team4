import pandas as pd
import plotly.express as px

# 1. 讀取資料
cols = ["Timestamp", "Hostname", "DiskNumber", "Type", "Offset", "Size", "ResponseTime"]
df = pd.read_csv("你的樣本檔名", names=cols) # 如果是空白分隔請改用 sep=r'\s+'

print("--- 基本資訊 ---")
print("總筆數:", len(df))
print(df["Type"].value_counts())

# 2. 轉換時間與單位
df["time"] = pd.to_datetime((df["Timestamp"] - 116444736000000000) // 10, unit="us")
df["resp_ms"] = df["ResponseTime"] / 10_000

print("\n--- 統計數據 ---")
print(df[["Size", "resp_ms"]].describe())

# ==========================================
# 3. 加上第二週要求的探索性圖表 (使用 Plotly)
# ==========================================

# 圖表一：讀寫比例長條圖 (Operation Distribution)
type_counts = df["Type"].value_counts().reset_index()
type_counts.columns = ["Type", "Count"]
fig_type = px.bar(type_counts, x="Type", y="Count", title="Read vs Write Operation Distribution")
fig_type.show()

# 圖表二：請求大小分佈直方圖 (Request-Size Histogram)
fig_size = px.histogram(df, x="Size", nbins=50, title="Request Size Distribution")
fig_size.show()

# 圖表三：I/O 時間序列圖 (I/O Time-Series，取前 1000 筆避免太密)
df_sorted = df.sort_values("time").head(1000)
fig_time = px.line(df_sorted, x="time", y="resp_ms", color="Type", title="Response Time Over Time (Sample)")
fig_time.show()