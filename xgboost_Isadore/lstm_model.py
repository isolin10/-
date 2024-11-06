# lstm_model.py
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense

def preprocess_data(data):
    # 將日期轉換為時間戳
    data['timesramp'] = data['date'].astype(np.int64) // 10**9  # 轉換為秒
    # 選擇所有需要的特徵（包括 timestamp）
    return data[['timesramp', 'temp', 'humd', 'ph', 'light', 'salt', 'ec', 'n', 'p', 'k']]

def train_lstm(data, predictions_dict):

        # 確保在 LSTM 訓練過程中能夠使用到 target_column
    for target_column in predictions_dict.keys():
        data[target_column] = data[target_column].fillna(0)  # 填補缺失值，保證完整數據
    
    # 預處理數據
    data = preprocess_data(data)

    
    
    # 取得特徵和目標變數
    X = data.drop(columns=['temp', 'humd', 'ph', 'light', 'salt', 'ec', 'n', 'p', 'k'])
    y = data[['temp', 'humd', 'ph', 'light', 'salt', 'ec', 'n', 'p', 'k']]

    # 轉換為 NumPy 數組，並調整形狀以適合 LSTM 輸入
    X = np.array(X)
    y = np.array(y)
    
    # 調整為適合 LSTM 的形狀，時間步長是 1（單一時間步驟）
    X = X.reshape((X.shape[0], 1, X.shape[1]))  # 改成 (樣本數, 1, 特徵數)

    print(X.shape)

    # 構建 LSTM 模型
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))  # 輸入形狀 (1, 特徵數)
    model.add(Dense(y.shape[1]))  # 輸出層，對應所有因子
    model.compile(optimizer='adam', loss='mse')

    # 訓練模型
    model.fit(X, y, epochs=200, verbose=0)

    return model