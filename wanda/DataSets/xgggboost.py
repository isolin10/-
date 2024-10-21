import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
import matplotlib

matplotlib.rc("font", family="Microsoft JhengHei")  # 中文


# 整理df["date"]
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    return df


train_df = load_and_preprocess_data("data_pca.csv")
test_df = load_and_preprocess_data("testdata.csv")


# 特徵工程temp
def add_temp_features(df):
    df["temp_diff"] = df["temp"].diff()
    df["temp_rolling_mean"] = df["temp"].rolling(window=24).mean()
    df["temp_rolling_std"] = df["temp"].rolling(window=24).std()
    df["temp_lag_1"] = df["temp"].shift(1)
    df["temp_lag_24"] = df["temp"].shift(24)
    return df


train_df = add_temp_features(train_df)
test_df = add_temp_features(test_df)

# 正規化特徵
scaler = MinMaxScaler()
features = [  # 修改要的特徵x，我是參考matrix結果 >0.6就當特徵
    "light",
    "hour",
    # "temp_diff",
    # "temp_rolling_mean",
    # "temp_rolling_std",
    # "temp_lag_1",
    # "temp_lag_24",
]
train_df[features] = scaler.fit_transform(train_df[features].fillna(0))
test_df[features] = scaler.transform(test_df[features].fillna(0))

# 使用 XGBoost 模型
X_train = train_df[features].dropna()
y_train = train_df["humd"].dropna()
X_test = test_df[features].dropna()
y_test = test_df["humd"].dropna()

# 訓練 XGBoost 模型
xgboost_model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
xgboost_model.fit(X_train, y_train)

# 進行預測
xgboost_forecast = xgboost_model.predict(X_test)

# 計算信心區間
predictions_list = []
for _ in range(100):  # 進行多次抽樣以獲得預測分佈
    sample_indices = np.random.choice(len(X_train), len(X_train), replace=True)
    X_sample, y_sample = X_train.iloc[sample_indices], y_train.iloc[sample_indices]
    model_sample = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
    model_sample.fit(X_sample, y_sample)
    predictions_list.append(model_sample.predict(X_test))

predictions_array = np.array(predictions_list)
mean_preds = np.mean(predictions_array, axis=0)
std_preds = np.std(predictions_array, axis=0)

confidence_lower_bound = mean_preds - 1.96 * std_preds
confidence_upper_bound = mean_preds + 1.96 * std_preds
mse = mean_squared_error(y_test, xgboost_forecast)
r2 = r2_score(y_test, xgboost_forecast)


print(f"MSE: {mse}")
print(f"R²: {r2}")


# 繪製結果
plt.figure(figsize=(15, 6))
plt.plot(train_df.index, train_df["humd"], label="Historical Humidity")
plt.plot(test_df.index, y_test, label="Actual Humidity", color="green")
plt.plot(
    test_df.index, xgboost_forecast, label="XGBoost Forecasted Humidity", color="red"
)
plt.fill_between(
    test_df.index,
    confidence_lower_bound,
    confidence_upper_bound,
    color="grey",
    alpha=0.3,
    label="95% Confidence Interval",
)
plt.title(
    f"Humidity Forecast vs Actual Values\nMSE: {mse}, R²: {r2}\nFeatures：{features}"
)
plt.xlabel("Date")
plt.ylabel("Humidity")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 顯示預測結果的前幾行
print("\nFirst few rows of XGBoost forecast results:")
forecast_results = pd.DataFrame({"Actual": y_test, "Forecast": xgboost_forecast})
print(forecast_results.head())
