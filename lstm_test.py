import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 讀取數據
data = pd.read_csv("1soildata.csv")

# 轉換日期格式
data["date"] = pd.to_datetime(data["date"])

# 設置日期為索引
data.set_index("date", inplace=True)

# 檢查缺失值
# print(data.isnull().sum())

# 標準化數據
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)
import numpy as np


def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i : (i + time_step), :])
        y.append(data[i + time_step, 8])  # 假設以第一列（如temp）作為目標變量
    return np.array(X), np.array(y)


# 設定時間步長
time_step = 24
X, y = create_dataset(scaled_data, time_step)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 建立LSTM模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1))  # 輸出層

# 編譯模型
model.compile(optimizer="adam", loss="mean_squared_error")

from sklearn.model_selection import train_test_split

# 分割數據集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 訓練模型
model.fit(X_train, y_train, epochs=100, batch_size=32)

predictions = model.predict(X_test)
predictions = np.reshape(
    predictions, (predictions.shape[0], 1)
)  # 改變形狀為 (n_samples, 1)
inverse_scaled_predictions = np.zeros((predictions.shape[0], scaled_data.shape[1]))
inverse_scaled_predictions[:, 0] = predictions.flatten()  # 將預測填入第一列
inverse_predictions = scaler.inverse_transform(inverse_scaled_predictions)
final_predictions = inverse_predictions[:, 8]  # 假設 temp 是第一列，以此類推

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(y_test, label="Actual")
plt.plot(predictions, label="Predicted")
plt.title(
    "Growth Period Prediction, optimizer = adam, epochs = 100, batch_size = 32, Dropout = 0.2"
)
plt.xlabel("Time Steps")
plt.ylabel("Growth Factor (e.g., Light)")
plt.legend()
plt.show()
