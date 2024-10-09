import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# 讀取CSV文件
df = pd.read_csv("1soildata.csv")
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# 只使用某特定數據
data = df["light"].values.reshape(-1, 1)

# 數據標準化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)


# 準備訓練數據
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i : (i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)


look_back = 8  # 使用過去8小時的數據來預測下一個小時
X, Y = create_dataset(scaled_data, look_back)

# 重塑輸入為 [samples, time steps, features]
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 構建LSTM模型
model = Sequential(
    [
        LSTM(
            50,
            activation="relu",
            input_shape=(look_back, 1),
            return_sequences=True,
            dropout=0.2,
        ),
        LSTM(50, activation="relu"),
        Dense(1),
    ]
)
model.compile(optimizer=Adam(learning_rate=0.001), loss="mse")

# 訓練模型
history = model.fit(X, Y, epochs=100, batch_size=32, validation_split=0.2, verbose=0)

# 繪製訓練損失
plt.figure(figsize=(10, 6))
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()

# 使用模型進行預測
predictions = model.predict(X)
predictions = scaler.inverse_transform(predictions)

# 繪製實際溫度和預測溫度
plt.figure(figsize=(12, 6))
plt.plot(df.index[look_back:], data[look_back:], label="Actual Light")
plt.plot(df.index[look_back:], predictions, label="Predicted Light")
plt.title("Light Prediction Time step = 8 Dropout = 0.2")
plt.xlabel("Date")
plt.ylabel("Light")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 計算預測誤差
mse = np.mean((predictions - data[look_back:]) ** 2)
rmse = np.sqrt(mse)
print(f"Root Mean Square Error: {rmse:.2f}")
