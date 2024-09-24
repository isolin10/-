# 查看資料的型態
print(data.dtypes)

# 將 date 欄位轉換為 datetime 型態
data['date'] = pd.to_datetime(data['date'])

# 檢查是否有空值
print(data.isnull().sum())

# 移除包含空值的資料行
data = data.dropna()

# 檢查每個因子的資料型態
for column in data.columns[1:]:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# 移除非數值資料（如果有的話）
data = data.dropna()

# 確認清洗後的資料型態
print(data.dtypes)
