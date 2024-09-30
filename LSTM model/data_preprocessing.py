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
    # 如果 data 不是 numpy array，則將其轉換
    if isinstance(data, pd.DataFrame):
        data = data.values  # 只在 data 是 DataFrame 時進行轉換

    sequences = []
    labels = []

    for i in range(len(data) - time_steps):
        seq = data[i:i+time_steps]
        label = data[i+time_steps]
        sequences.append(seq)
        labels.append(label)
    
    return np.array(sequences), np.array(labels)

def train_test_split(data, train_size):
    train_data_len = int(len(data) * train_size)
    train_data = data[:train_data_len]
    test_data = data[train_data_len:]
    return train_data, test_data

def prepare_data(file_path):
    # 載入和預處理數據
    data = pd.read_csv(file_path)
    # 這裡進行縮放、拆分訓練/測試數據
    X_train, y_train, X_test, y_test, scaler = your_data_processing_function(data)

    return {
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test,
        'scaler': scaler
    }
