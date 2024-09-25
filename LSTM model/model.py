#定義 LSTM 模型的架構和構建過程。
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64))
    model.add(Dropout(0.2))
    model.add(Dense(units=8))  # 假設有 8 個輸出對應土壤因子
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
