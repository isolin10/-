#負責數據處理，包括標準化、數據分割、時間序列處理等。
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def convert_time_to_numeric(data, time_column):
    """
    將時間列轉換為數值格式（時間戳或其他數值表示方式）。
    假設時間是以 'MM/DD/YYYY HH:MM:SS AM/PM' 格式提供的。
    """
    # 轉換時間欄位為datetime格式
    data[time_column] = pd.to_datetime(data[time_column], format='%m/%d/%Y %I:%M:%S %p')
    # 將datetime格式轉換為秒級的Unix時間戳
    data[time_column] = data[time_column].view('int64') // 10**9
    return data

def scale_data(data, time_column=None):
    """
    標準化數據。如果包含時間列，先將時間轉換為數值。
    """
    if time_column:
        data = convert_time_to_numeric(data, time_column)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

def create_sequences(data, time_steps):
    sequences, labels = [], []
    for i in range(len(data) - time_steps):
        sequences.append(data[i:i+time_steps])
        labels.append(data[i+time_steps])
    return np.array(sequences), np.array(labels)

def train_test_split(data, train_size):
    train_data_len = int(len(data) * train_size)
    train_data = data[:train_data_len]
    test_data = data[train_data_len:]
    return train_data, test_data
