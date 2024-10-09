import numpy as np
import matplotlib.pyplot as plt
from data_preprocessing import load_data, preprocess_data
from train_predict import train_and_predict_with_grid_search
from model_evaluation import evaluate_model

# 設定參數
file_path = 'plant_data.csv'
target_columns = ['temp', 'humd', 'salt', 'ec', 'ph', 'n', 'p', 'k', 'light']  # 目標列
window_size = 10  # 時間窗口大小

# 迴圈處理每個目標因子
for target_col in target_columns:
    # 數據預處理
    df = load_data(file_path)
    X, y, scaler = preprocess_data(df, target_col, window_size)
    
    # 切分數據集
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # 使用網格搜索訓練模型並預測
    y_pred, best_params = train_and_predict_with_grid_search(X_train, y_train, X_test, scaler)

    # 反標準化 y_test 以便於比較
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    # 評估模型效能
    mse, mae, rmse = evaluate_model(y_test_actual, y_pred)

    # 繪製實際值與預測值的曲線
    plt.figure(figsize=(12, 6))
    plt.plot(y_test_actual, label='Actual Values', color='blue')
    plt.plot(y_pred, label='Predicted Values', color='orange')
    plt.title(f'Actual vs Predicted for {target_col} (Best Params: {best_params})')
    plt.xlabel('Time Steps')
    plt.ylabel(target_col)
    plt.legend()
    plt.grid()
    plt.show()

    print(f"Performance metrics for {target_col}:")
    print(f"MSE: {mse:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")
    print(f"Best Hyperparameters: {best_params}")