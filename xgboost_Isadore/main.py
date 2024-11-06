# main.py
from data_processing import load_data, preprocess_data
from xgboost_model import train_xgboost
from utils import plot_predictions
import os
from lstm_model import train_lstm
import numpy as np


# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    file_path = 'data2.csv'
 
    if not os.path.exists(file_path):
        print(f'File {file_path} not found!')
        return

    data = load_data(file_path)
    data = preprocess_data(data)

    # 定義要預測的所有因子
    target_columns = ['temp', 'humd', 'salt', 'ec', 'ph', 'n', 'p', 'k', 'light']

    # 訓練並預測 XGBoost 模型
    models, test_sets, predictions_dict, confidence_intervals, hit_rates = train_xgboost(data, target_columns)

    # 使用 XGBoost 預測結果作為 LSTM 的輸入
    print("Training LSTM model using XGBoost features...")
    lstm_model = train_lstm(data, predictions_dict)

    # 顯示命中率，並使用 LSTM 進行預測
    for target_column in target_columns:
        X_test, y_test = test_sets[target_column]
        predictions = predictions_dict[target_column]
        confidence_interval = confidence_intervals[target_column]
        factor_name = target_column

        # 繪製 XGBoost 預測結果的圖表
        print(f'Plotting for XGBoost predictions for {target_column}...')
        plot_predictions(data['date'].iloc[X_test.index], y_test, predictions, confidence_interval, factor_name)
     
        # 使用 LSTM 進行預測
        X_test_lstm = np.array(X_test)
        X_test_lstm = X_test_lstm.reshape((X_test_lstm.shape[0], 1, X_test_lstm.shape[1]))  # 調整為 LSTM 所需的形狀
        lstm_predictions = lstm_model.predict(X_test_lstm)  # LSTM 預測結果

        # 計算 LSTM 預測結果的 MSE, RMSE 和 MAE
        lstm_mse = np.mean((lstm_predictions - y_test) ** 2)
        lstm_rmse = np.sqrt(lstm_mse)
        lstm_mae = np.mean(np.abs(lstm_predictions - y_test))
        lstm_confidence_interval = 1.96 * (lstm_mse) ** 0.5

        print(f'LSTM MSE for {target_column}: {lstm_mse}')
        print(f'LSTM RMSE for {target_column}: {lstm_rmse}')
        print(f'LSTM MAE for {target_column}: {lstm_mae}')
        print(f'95% Confidence Interval for LSTM {target_column}: +/- {lstm_confidence_interval}')

        # 繪製 LSTM 預測結果的圖表
        print(f'Plotting for LSTM predictions for {target_column}...')
        plot_predictions(data['date'].iloc[X_test.index], y_test, lstm_predictions, lstm_confidence_interval, factor_name)

if __name__ == '__main__':
    main()