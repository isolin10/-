# xgboost_model.py
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_xgboost(data, target_column):
    # 不包含 'date' 列
    X = data.drop(columns=[target_column, 'date'])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    print(f'XGBoost MSE: {mse}')
    
    # 計算信心區間
    confidence_interval = 1.96 * (mean_squared_error(y_test, predictions))**0.5
    
    print(f'95% Confidence Interval: +/- {confidence_interval}')

    return model, X_test, y_test, predictions, confidence_interval
