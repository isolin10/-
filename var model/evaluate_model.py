import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error
from statsmodels.stats.diagnostic import acorr_ljungbox
from numpy.linalg import LinAlgError 
import matplotlib.pyplot as plt
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def evaluate_var_model(df: pd.DataFrame, lags: int):
    """
    評估 VAR 模型的表現。
    :param df: 資料 DataFrame
    :param lags: VAR 模型的滯後數
    :return: 評估結果，包括 MSE, RMSE, AIC, BIC 和 Ljung-Box 檢驗的結果
    """
    
    # 分割資料為訓練集和測試集 (80% 訓練，20% 測試)
    n_obs = len(df)
    train_size = int(n_obs * 0.8)
    train, test = df[0:train_size], df[train_size:]
    
    # 訓練 VAR 模型
    model = VAR(train)
    var_model = model.fit(lags, trend='c')  # 可調整 trend='nc' 無截距，或 trend='ct' 加上趨勢項
    
    # 使用訓練的模型進行預測
    forecast = var_model.forecast(train.values[-lags:], steps=len(test))
    
    # 計算 MSE 和 RMSE
    mse = mean_squared_error(test.values, forecast)
    rmse = np.sqrt(mse)
    
    # 計算 AIC 和 BIC
    try:
        aic = var_model.aic
        bic = var_model.bic
    except LinAlgError:
        aic = np.nan
        bic = np.nan
        print("警告: 協方差矩陣不是正定的，無法計算 AIC 和 BIC。")
    
    # 殘差自相關檢驗 (Ljung-Box Test)
    residuals = test.values - forecast
    residuals_flat = residuals.flatten()  # 將殘差展平為一維數組
    lb_test = acorr_ljungbox(residuals_flat, lags=[lags], return_df=True)
    
    print("VAR Model Evaluation")
    print("----------------------")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"AIC: {aic:.4f}" if not np.isnan(aic) else "AIC: 無法計算")
    print(f"BIC: {bic:.4f}" if not np.isnan(bic) else "BIC: 無法計算")
    print("\nLjung-Box Test for Residuals Autocorrelation:")
    print(lb_test)
    
    return mse, rmse, aic, bic, lb_test, train, test, forecast

def plot_predictions(train, test, forecast):
    """
    繪製實際值與預測值的圖形。
    """
    plt.figure(figsize=(12, 6))
    plt.plot(train.index[-50:], train.values[-50:], label='Train', color='blue')
    plt.plot(test.index, test.values, label='Test', color='orange')
    plt.plot(test.index, forecast, label='Forecast', color='green')
    plt.title('VAR Model Predictions')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    from data_loader import load_data
    
    # 載入資料
    file_path = "plant_data.csv"
    df = load_data(file_path)

    # 確保日期索引的頻率
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])  # 假設日期在 'date' 列
        df.set_index('date', inplace=True)
        df = df.asfreq('H')  # 設定頻率為每小時 (根據你的資料設置頻率)

    # 評估模型 (設定滯後數 lags = 3)
    mse, rmse, aic, bic, lb_test, train, test, forecast = evaluate_var_model(df, lags=3)

    # 在模型評估結束後繪製圖形
    plot_predictions(train, test, forecast)
