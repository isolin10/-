import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_predictions(dates, y_true, y_pred, confidence_interval):
    # 將日期轉換為小時級別 (假設每個日期都有 24 個小時的時間點)
    hourly_dates = pd.date_range(start=dates.min(), end=dates.max(), freq='H')[:len(y_true)]
    
    plt.figure(figsize=(12, 6))
    
    # 繪製真實值
    plt.plot(hourly_dates, y_true, label='True Values', color='blue', marker='o', markersize=2)
    
    # 繪製預測值
    plt.plot(hourly_dates, y_pred, label='Predictions', color='orange', marker='x', markersize=2)
    
    # 計算信心區間上下界
    lower_bound = y_pred - confidence_interval
    upper_bound = y_pred + confidence_interval
    
    # 繪製信心區間
    plt.fill_between(hourly_dates, lower_bound, upper_bound, color='gray', alpha=0.5, label='95% Confidence Interval')

    plt.title('True Values vs Predictions')
    plt.xlabel('Date (Hourly)')
    plt.ylabel('Temperature')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
