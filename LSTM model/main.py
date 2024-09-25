import numpy as np
from train import train_lstm_model
from utils import plot_loss, evaluate_model
import pandas as pd
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 假設你有一個 CSV 檔案儲存土壤因子數據
data = pd.read_csv('plant_data.csv').values

# 設定參數
time_steps = 30  # 使用前30天的數據來預測
train_size = 0.8
epochs = 100
batch_size = 32

# 訓練模型
model, history, scaler = train_lstm_model(data, time_steps, train_size, epochs, batch_size)

# 繪製損失圖
plot_loss(history)

# 模型評估
X_test, y_test = create_sequences(data, time_steps)[1]
predictions_rescaled, y_test_rescaled = evaluate_model(model, X_test, y_test, scaler)

# 進一步處理或顯示預測結果
