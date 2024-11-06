#utils.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_predictions(dates, y_true, y_pred, confidence_interval, factor_name):
    # 將日期轉換為小時級別並且長度匹配
    hourly_dates = pd.date_range(start=dates.iloc[0], periods=len(y_true), freq='H')
    
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

    plt.title(f'{factor_name} Prediction vs True Value')
    plt.xlabel('Date')
    plt.ylabel(f'{factor_name}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
