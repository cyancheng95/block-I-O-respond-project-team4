# block-I-O-respond-project-team4


單位對照表
欄位	README 的說明	分析時轉換成
Timestamp	Windows filetime，I/O 發出的時間	datetime 或距起點的秒數／小時
Hostname	主機名稱，與檔名一致	不轉換
DiskNumber	邏輯區塊裝置編號，與檔名一致	不轉換
Type	Read 或 Write	不轉換
Offset	從邏輯磁碟起點算起的起始位置，bytes	GB 或 sector（視圖而定）
Size	傳輸大小，bytes	KB
ResponseTime	I/O 完成所花時間，Windows filetime 單位	ms
