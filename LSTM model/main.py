import numpy as np
from train import train_lstm_model
from utils import plot_loss
import pandas as pd
from visualization import plot_predictions

# 設定參數
time_steps = 50
train_size = 0.8
epochs = 100
batch_size = 32
time_column = 'date'

# 加載數據
data = pd.read_csv('plant_data.csv')

# 訓練模型
model, history, input_scaler, output_scaler, X_test, y_test = train_lstm_model(
    data, time_steps, train_size, epochs, batch_size, time_column
)

# 繪製損失圖
#plot_loss(history)


# 模型評估
predictions = model.predict(X_test)

# 反向標準化
y_test_rescaled = output_scaler.inverse_transform(y_test)
predictions_rescaled = output_scaler.inverse_transform(predictions)

# 預測並可視化結果
plot_predictions(model, data, input_scaler, time_steps, time_column)