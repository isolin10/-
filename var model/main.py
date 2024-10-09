#主程式，統整並執行各模組。
from data_loader import load_data, diff_data
from data_visualization import plot_data
from model_builder import build_var_model, print_model_summary
from model_forecast import forecast_var_model
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# 1. 讀取並預處理資料
file_path = 'plant_data.csv'  # 資料集路徑
df = load_data(file_path)
df_diff = diff_data(df)

# 2. 視覺化資料
plot_data(df)

# 3. 構建 VAR 模型
results = build_var_model(df_diff)

# 4. 輸出模型摘要
print_model_summary(results)

# 5. 使用模型進行預測
forecast_df = forecast_var_model(results, df_diff)
print(forecast_df)
