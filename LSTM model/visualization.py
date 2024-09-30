#負責從測試數據中生成預測，並將預測結果和真實結果進行可視化比較。
# visualization.py
import matplotlib.pyplot as plt
from data_preprocessing import create_sequences
import pandas as pd
import numpy as np

data = pd.read_csv('plant_data.csv')

import matplotlib.pyplot as plt

def plot_predictions(model, data, scaler, time_steps, time_column):
     # 先获取测试数据
    X_test, y_test = create_sequences(data, time_steps)

    # 对预测结果进行反归一化
    y_test_rescaled = scaler.inverse_transform(y_test)
    predictions = model.predict(X_test)
    predictions_rescaled = scaler.inverse_transform(predictions)

    # 绘制每个因子的图
    num_factors = y_test_rescaled.shape[1]
    for i in range(num_factors):
        plt.figure(figsize=(12, 6))
        plt.plot(y_test_rescaled[:, i], label='Actual Value', color='blue')
        plt.plot(predictions_rescaled[:, i], label='Predicted Value', color='orange')
        plt.title(f'Prediction Results for Factor {i + 1}')
        plt.xlabel('Time Steps')
        plt.ylabel(f'Values of Factor {i + 1}')
        plt.legend()
        plt.show()