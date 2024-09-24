# csvwashdata.py
import pandas as pd

def load_and_clean_data(filepath):
    # 從CSV檔案中讀取資料
    data = pd.read_csv(filepath)

    # 查看資料的型態
    print(data.dtypes)

    # 將 date 欄位轉換為 datetime 型態
    data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y %I:%M:%S %p')

    # 檢查是否有空值
    print(data.isnull().sum())

    # 移除包含空值的資料行
    data = data.dropna()

    # 檢查每個因子的資料型態，並確保它們是數值型態
    for column in data.columns[1:]:
        data[column] = pd.to_numeric(data[column], errors='coerce')

    # 移除非數值資料（如果有的話）
    data = data.dropna()

    # 確認清洗後的資料型態
    print(data.dtypes)

    return data

# 如果你希望直接執行此腳本來測試清洗過程
if __name__ == "__main__":
    filepath = 'plant_data.csv'
    data = load_and_clean_data(filepath)
    print(data.head())
