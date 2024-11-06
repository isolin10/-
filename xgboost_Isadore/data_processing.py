#data_processing.py
import pandas as pd
import os
import numpy as np

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_data(file_path):
    data = pd.read_csv(file_path)
    # 進行時間格式轉換
    data['date'] = pd.to_datetime(data['date'])
    # 將日期轉換為時間戳
    data['date'] = data['date'].astype(np.int64) // 10**9  # 轉換為秒

    # 將除 'date' 欄位以外的所有欄位轉換為 float
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name != 'date' else x)

    # 檢查列名
    print("Columns in the loaded data:", data.columns.tolist())
    
    return data

def preprocess_data(data):
    # 在此進行其他的數據處理，例如標準化、填補缺失值等
    data = data.dropna()
    return data
