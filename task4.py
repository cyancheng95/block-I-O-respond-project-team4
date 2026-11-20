import pandas as pd
import plotly.express as px

# 1. 定義欄位名稱
cols = ['time', 'host', 'disk', 'Type', 'Offset', 'Size', 'resp_ms']

# 2. 讀取資料檔案（請將路徑修改為你的實際檔名與格式）
df = pd.read_excel(r"你的檔案路徑\你的檔名.xlsx", header=None, names=cols)
# 若為純文字或 CSV 檔，請註解掉上面那行，改用下面這行：
# df = pd.read_csv(r"你的檔案路徑\你的檔名.csv", names=cols, encoding='latin-1')


# ==========================================
# Task 4: 儲存存取模式探索 (Storage Access Patterns)
# ==========================================
# 1. 依時間順序排序，並計算相鄰 I/O 請求的 Offset 絕對差值
df = df.sort_values('time').reset_index(drop=True)
df['Offset_Diff'] = df['Offset'].diff().abs()

# 判斷是否為完全連續（循序）存取：前一次的 Offset + 前一次的 Size == 當前的 Offset
df['Prev_End'] = df['Offset'].shift(1) + df['Size'].shift(1)
df['Is_Sequential'] = (df['Offset'] == df['Prev_End'])

seq_ratio = df['Is_Sequential'].mean() * 100
print("=== Task 4: 儲存存取模式與空間局部性統計 ===")
print(f"完全循序存取 (Sequential Access) 比例: {seq_ratio:.2f}%")
print("\n相鄰請求 Offset 差值分佈統計:")
print(df['Offset_Diff'].describe())

# 2. 產出圖表 A：存取軌跡圖 (Offset Over Time)
# 取前 2000 筆資料觀察磁碟區塊的存取軌跡（斜線代表循序讀寫，散點代表隨機跳躍）
fig_offset = px.scatter(df.head(2000), x='time', y='Offset', color='Type',
                        title="Task 4: Storage Access Patterns (Offset Over Time)",
                        labels={'time': 'Timestamp', 'Offset': 'Disk Offset (Bytes)'})
fig_offset.show()

# 3. 產出圖表 B：Offset 跳躍距離分佈直方圖（觀察空間局部性集中度）
# 過濾掉差值為 0 的極端情況並使用 Log 軸觀察跨度
valid_diff = df[df['Offset_Diff'] > 0]
fig_diff = px.histogram(valid_diff.sample(min(10000, len(valid_diff))), x='Offset_Diff', color='Type',
                        log_x=True, nbins=50,
                        title="Task 4: Offset Difference Distribution (Log Scale)",
                        labels={'Offset_Diff': 'Offset Jump Distance (Bytes)'})
fig_diff.show()