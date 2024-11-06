# xgboost_model.py
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def train_xgboost(data, target_columns):
    models = {}
    test_sets = {}
    predictions_dict = {}
    confidence_intervals = {}
    hit_rates = {}

    for target_column in target_columns:
        # 移除目標因子欄位，但保留日期
        X = data.drop(columns=[target_column])  # 不刪除 date 欄位
        y = data[target_column]

        # 分割資料集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 訓練 XGBoost 模型
        model = xgb.XGBRegressor()
        model.fit(X_train, y_train)

        # 預測
        predictions = model.predict(X_test)

        # 計算 MSE, RMSE 和 MAE
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, predictions)

        print(f'XGBoost MSE for {target_column}: {mse}')
        print(f'XGBoost RMSE for {target_column}: {rmse}')
        print(f'XGBoost MAE for {target_column}: {mae}')
        
        # 計算信心區間
        confidence_interval = 1.96 * (mse)**0.5
        print(f'95% Confidence Interval for {target_column}: +/- {confidence_interval}')

        # 計算命中率
        lower_bound = predictions - confidence_interval
        upper_bound = predictions + confidence_interval
        hit = (y_test >= lower_bound) & (y_test <= upper_bound)
        hit_rate = hit.mean()
        print(f'Hit rate for {target_column} within 95% Confidence Interval: {hit_rate}')

        # 儲存結果
        models[target_column] = model
        test_sets[target_column] = (X_test, y_test)
        predictions_dict[target_column] = predictions
        confidence_intervals[target_column] = confidence_interval
        hit_rates[target_column] = hit_rate

    return models, test_sets, predictions_dict, confidence_intervals, hit_rates
