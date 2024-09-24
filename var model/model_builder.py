#負責構建 VAR 模型。
import pandas as pd 
from statsmodels.tsa.api import VAR

def build_var_model(df: pd.DataFrame, maxlags: int = 15):
    """
    構建 VAR 模型，並使用 AIC 準則選擇滯後期數。
    :param df: 差分後的資料
    :param maxlags: VAR 模型的最大滯後期數
    :return: 已訓練的 VAR 模型
    """
    model = VAR(df)
    results = model.fit(maxlags=maxlags, ic='aic')
    return results

def print_model_summary(results):
    """
    輸出模型摘要。
    :param results: VAR 模型結果
    """
    print(results.summary())
