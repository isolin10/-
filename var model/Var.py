from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

# 將 date 欄位設置為索引
data.set_index('date', inplace=True)

# 檢查資料
print(data.head())

# 初始化和擬合VAR模型
model = VAR(data)
model_fit = model.fit()

# 檢查模型的摘要
print(model_fit.summary())

# 繪製VAR模型的殘差
model_fit.plot()

# 預測未來值（假設我們希望預測下一個時間步長）
forecast = model_fit.forecast(model_fit.y, steps=1)

# 將預測值添加到原始資料中
forecast_df = pd.DataFrame(forecast, columns=data.columns, index=[data.index[-1] + pd.Timedelta(days=1)])

# 打印預測值
print("預測結果:")
print(forecast_df)

# 繪製預測結果
plt.figure(figsize=(10, 6))
for column in data.columns:
    plt.plot(data.index, data[column], label=column)
plt.plot(forecast_df.index, forecast_df.iloc[0], label='Forecast', linestyle='--')
plt.title('VAR Model Forecast')
plt.xlabel('date')
plt.ylabel('Value')
plt.legend()
plt.show()
