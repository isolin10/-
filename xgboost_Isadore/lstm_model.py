#lstm_model.py

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import EarlyStopping
import numpy as np

def build_lstm_model(input_shape, lstm_units=50):
    """
    構建可調整 LSTM 單元數量的模型
    """
    model = Sequential([
        LSTM(lstm_units, return_sequences=True, input_shape=input_shape),
        LSTM(lstm_units, return_sequences=False),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm_model(model, train_data, train_target, epochs=50, batch_size=32, patience=10):
    """
    訓練 LSTM 模型，加入早停回調
    """
    train_data = np.array(train_data)
    train_target = np.array(train_target)
    
    # 定義早停回調
    early_stopping = EarlyStopping(
        monitor='loss',  # 監控訓練損失
        patience=patience,  # 容忍 patience 次沒有改進
        restore_best_weights=True  # 還原到最佳權重
    )
    
    model.fit(train_data, train_target, epochs=epochs, batch_size=batch_size, verbose=0, callbacks=[early_stopping])
    return model

