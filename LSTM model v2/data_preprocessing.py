#負責數據的讀取、清理和預處理
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df

def preprocess_data(df, target_col, window_size):
    # 取出特徵與目標變數
    features = df.drop(columns=[target_col]).values
    target = df[target_col].values

    # 使用MinMaxScaler進行標準化
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    target_scaled = scaler.fit_transform(target.reshape(-1, 1)).flatten()

    # 構建序列數據
    X, y = [], []
    for i in range(window_size, len(features_scaled)):
        X.append(features_scaled[i-window_size:i])
        y.append(target_scaled[i])
    
    return np.array(X), np.array(y), scaler
