#訓練與預測
from lstm_model import build_lstm_model, train_model
import numpy as np

def train_and_predict(X_train, y_train, X_test, scaler, epochs=50, batch_size=32):
    # 建立LSTM模型
    model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
    
    # 訓練模型
    train_model(model, X_train, y_train, epochs=epochs, batch_size=batch_size)

    # 預測
    y_pred_scaled = model.predict(X_test)
    
    # 反標準化
    y_pred = scaler.inverse_transform(y_pred_scaled)
    
    return y_pred
