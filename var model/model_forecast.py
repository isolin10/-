#負責使用模型進行預測。
import pandas as pd

def forecast_var_model(results, df: pd.DataFrame, steps: int = 10):
    """
    使用訓練好的 VAR 模型進行未來數據預測。
    :param results: 訓練好的 VAR 模型
    :param df: 差分後的資料
    :param steps: 預測步數（預測的時間點數）
    :return: 預測結果的 DataFrame
    """
    lag_order = results.k_ar
    forecast = results.forecast(df.values[-lag_order:], steps=steps)
    forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=df.index[-1], periods=steps, freq='T'), columns=df.columns)
    return forecast_df
