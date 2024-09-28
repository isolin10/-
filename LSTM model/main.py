import numpy as np
from train import train_lstm_model
from utils import plot_loss, evaluate_model
import pandas as pd
from data_preprocessing import create_sequences

# 加載數據
data = pd.read_csv('plant_data.csv')

# 假設時間列名稱是 'timestamp'
time_column = 'date'

# 設定參數
time_steps = 30
train_size = 0.8
epochs = 100
batch_size = 32

# 訓練模型
model, history, scaler = train_lstm_model(data, time_steps, train_size, epochs, batch_size, time_column)



# 繪製損失圖
plot_loss(history)

# 模型評估
X_test, y_test = create_sequences(data, time_steps)[1]
predictions_rescaled, y_test_rescaled = evaluate_model(model, X_test, y_test, scaler)