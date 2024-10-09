#評估模型的效能
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import numpy as np

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return mse, mae, rmse
