import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error
from statsmodels.stats.diagnostic import acorr_ljungbox
from numpy.linalg import LinAlgError
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pd.set_option('display.float_format', lambda x: '%.3f' % x)

def evaluate_var_model(train, test, lags):
    """
    評估 VAR 模型的表現。
    :param train: 訓練集資料
    :param test: 測試集資料
    :param lags: VAR 模型的滯後數
    :return: 評估結果，包括 MSE, RMSE, AIC, BIC 和 Ljung-Box 檢驗的結果
    """
    # 訓練 VAR 模型
    model = VAR(train)
    var_model = model.fit(lags)
    
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
        print(f"協方差矩陣非正定: lags={lags}，無法計算 AIC 和 BIC。")
    
    # 殘差自相關檢驗 (Ljung-Box Test)
    residuals = test.values - forecast
    residuals_flat = residuals.flatten()
    lb_test = acorr_ljungbox(residuals_flat, lags=[lags], return_df=True)
    
    return mse, rmse, aic, bic, lb_test

def cross_validation(df, lags_list):
    """
    使用交叉驗證來測試不同滯後期數，並根據指標選擇最佳參數。
    :param df: 資料 DataFrame
    :param lags_list: 滯後期數列表
    :return: 最佳滯後期數及其對應的指標
    """
    # 分割資料為訓練集和測試集
    train_size = int(len(df) * 0.8)
    train, test = df[:train_size], df[train_size:]
    
    results = []
    
    # 遍歷滯後期數，計算每個滯後期數的評估指標
    for lags in lags_list:
        mse, rmse, aic, bic, lb_test = evaluate_var_model(train, test, lags)
        results.append({
            'lags': lags,
            'mse': mse,
            'rmse': rmse,
            'aic': aic,
            'bic': bic,
            'lb_stat': lb_test['lb_stat'].values[0],
            'lb_pvalue': lb_test['lb_pvalue'].values[0]
        })
    
    # 將結果轉換為 DataFrame 並排序
    results_df = pd.DataFrame(results)
    
    # 將結果按 MSE、AIC、BIC 排序
    results_df = results_df.sort_values(by=['mse', 'aic', 'bic']).reset_index(drop=True)
    
    print("交叉驗證結果:")
    print(results_df)
    
    # 返回最佳參數組合
    best_result = results_df.iloc[0]
    return best_result

if __name__ == "__main__":
    from data_loader import load_data
    
    # 載入資料
    file_path = "plant_data.csv"
    df = load_data(file_path)

    # 確保日期索引的頻率
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])  # 假設日期在 'date' 列
        df.set_index('date', inplace=True)
        df = df.asfreq('H')  # 設定頻率，根據實際情況調整

    # 滯後期數列表
    lags_list = range(1,100)

    # 執行交叉驗證
    best_params = cross_validation(df, lags_list)

    print("\n最佳參數組合:")
    print(best_params)
