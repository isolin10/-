# 評估模型的預測準確性
from sklearn.metrics import mean_squared_error

# 將預測值與真實值進行比較
true_values = data.iloc[-1].values  # 最後一個時間點的真實值
predicted_values = forecast_df.iloc[0].values  # 預測值

# 計算均方根誤差（RMSE）
rmse = mean_squared_error(true_values, predicted_values, squared=False)
print("均方根誤差（RMSE）:", rmse)
