# main.py
from data_processing import load_data, preprocess_data
from xgboost_model import train_xgboost
from utils import plot_predictions
import os

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

    # 訓練和預測每個因子
    models, test_sets, predictions_dict, confidence_intervals = train_xgboost(data, target_columns)

    # 繪製每個因子的預測結果
    for target_column in target_columns:
        X_test, y_test = test_sets[target_column]
        predictions = predictions_dict[target_column]
        confidence_interval = confidence_intervals[target_column]
        
        print(f'Plotting for {target_column}...')
        plot_predictions(data['date'].iloc[X_test.index], y_test, predictions, confidence_interval)

if __name__ == '__main__':
    main()
