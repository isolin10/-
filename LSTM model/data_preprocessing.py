#負責數據處理，包括標準化、數據分割、時間序列處理等。
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def scale_data(data):
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
