# lstm_model.py
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense

def preprocess_data(data):
    # 將日期轉換為時間戳
    data['timestamp'] = data['date'].astype(np.int64) // 10**9  # 轉換為秒
    # 選擇需要的特徵（包括 timestamp）
    return data[['timestamp', 'temp', 'humd', 'ph', 'light', 'ele_npk', 'ele_ec_salt']]

def train_lstm(data):
    # 預處理數據
    data = preprocess_data(data)
    
    # 取得特徵和目標變數
    X = data.drop(columns=['temp'])
    y = data['temp']

    # 轉換為 NumPy 數組，並調整形狀以適合 LSTM 輸入
    X = np.array(X)
    y = np.array(y)

    # 假設使用單一時間步驟
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    model.fit(X, y, epochs=200, verbose=0)

    return model
