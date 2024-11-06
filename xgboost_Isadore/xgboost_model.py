# xgboost_model.py
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_xgboost(data, target_columns):
    models = {}
    test_sets = {}
    predictions_dict = {}
    confidence_intervals = {}

    for target_column in target_columns:
        # 移除日期和目標因子欄位
        X = data.drop(columns=target_columns + ['date'])
        y = data[target_column]

        # 分割資料集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 訓練 XGBoost 模型
        model = xgb.XGBRegressor()
        model.fit(X_train, y_train)

        # 預測
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f'XGBoost MSE for {target_column}: {mse}')
        
        # 計算信心區間
        confidence_interval = 1.96 * (mse)**0.5
        print(f'95% Confidence Interval for {target_column}: +/- {confidence_interval}')

        # 儲存結果
        models[target_column] = model
        test_sets[target_column] = (X_test, y_test)
        predictions_dict[target_column] = predictions
        confidence_intervals[target_column] = confidence_interval

    return models, test_sets, predictions_dict, confidence_intervals
