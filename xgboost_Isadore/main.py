# main.py
from data_processing import load_data, preprocess_data
from xgboost_model import train_xgboost
from lstm_model import train_lstm
from utils import plot_predictions
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    file_path = 'data.csv'
    
    if not os.path.exists(file_path):
        print(f'File {file_path} not found!')
        return

    data = load_data(file_path)
    data = preprocess_data(data)

    # 假設我們要預測 'temp' 這一欄
    xgb_model, X_test, y_test, predictions, confidence_interval = train_xgboost(data, target_column='temp')

    # 繪製預測結果及信心區間
    plot_predictions(data['date'].iloc[X_test.index], y_test, predictions, confidence_interval)

if __name__ == '__main__':
    main()
