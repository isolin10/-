# data_processing.py
import pandas as pd
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_data(file_path):
    data = pd.read_csv(file_path)
    # 進行數據的預處理，例如時間格式轉換等
    data['date'] = pd.to_datetime(data['date'])

    # 檢查列名
    print("Columns in the loaded data:", data.columns.tolist())
    
    return data

def preprocess_data(data):
    # 在此進行其他的數據處理，例如標準化、填補缺失值等
    data = data.dropna()
    return data
