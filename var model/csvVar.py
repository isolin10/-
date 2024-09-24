# csvVar.py
import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from csvwashdata import load_and_clean_data

# 載入並清洗資料
filepath = 'plant_data.csv'
data = load_and_clean_data(filepath)

# 設定日期為索引
data.set_index('date', inplace=True)

# 建立VAR模型
model = VAR(data)

# 自動選擇最佳滯後數
results = model.fit(ic='aic')

# 獲取預測結果
lag_order = results.k_ar
forecast_input = data.values[-lag_order:]
forecast = results.forecast(y=forecast_input, steps=10)

# 將預測結果轉換為DataFrame
forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=data.index[-1], periods=10, freq='H'), columns=data.columns)
print(forecast_df)

# 計算MSE
mse = mean_squared_error(data.values[-10:], forecast[:10])
print(f'Mean Squared Error: {mse}')

# 視覺化預測結果
for column in data.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(data.index[-50:], data[column].values[-50:], label='Actual')
    plt.plot(forecast_df.index, forecast_df[column].values, label='Forecast', linestyle='dashed')
    plt.title(f'{column} Forecast vs Actual')
    plt.legend()
    plt.show()
