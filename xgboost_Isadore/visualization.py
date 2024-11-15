#visualization.py

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def plot_predictions(dates, true_values, predicted_values, factor_name):
    """
    繪製預測結果與真實值對比的圖表
    """
    plt.figure(figsize=(12, 6))
    plt.plot(dates, true_values, label="True Values", color="blue", linestyle="-")
    plt.plot(dates, predicted_values, label="Predictions", color="red", linestyle="--")
    plt.xlabel("Date")
    plt.ylabel(factor_name)
    plt.title(f"{factor_name}: True vs Predicted")
    plt.legend()
    plt.grid()
    plt.show()

def calculate_hit_rate(true_values, predicted_values):
    """
    計算預測值命中真實值的95%信心區間的比例
    """
    # 計算真實值的均值和標準差
    mean = np.mean(true_values)
    std_dev = np.std(true_values)
    
    # 計算信心區間
    lower_bound = mean - 1.96 * std_dev
    upper_bound = mean + 1.96 * std_dev

    # 計算預測值命中區間的比例
    hits = np.logical_and(predicted_values >= lower_bound, predicted_values <= upper_bound)
    hit_rate = np.sum(hits) / len(true_values) * 100
    return hit_rate, lower_bound, upper_bound

def plot_with_confidence_interval(dates, true_values, predicted_values, factor_name, train_data):
    """
    繪製包含真實值的動態95%信心區間的圖表
    """
    # 計算真實值的標準差
    std_dev_true = np.std(true_values)

    # 根據每個時間點的真實值計算信心區間
    lower_bound_true = true_values - 1.96 * std_dev_true
    upper_bound_true = true_values + 1.96 * std_dev_true

    # 依照真實值的信心區間來畫圖
    plt.figure(figsize=(12, 6))
    plt.plot(dates, true_values, label="True Values", color="blue", linestyle="-")
    plt.plot(dates, predicted_values, label="Predictions", color="red", linestyle="--")
    plt.fill_between(dates, lower_bound_true, upper_bound_true, color='gray', alpha=0.2, label="95% Confidence Interval (True Values)")
    plt.xlabel("Date")
    plt.ylabel(factor_name)
    plt.title(f"{factor_name}: Predictions with 95% Confidence Interval")
    plt.legend()
    plt.grid()
    plt.show()