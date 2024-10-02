# 訓練模型邏輯，包括數據加載、模型訓練和保存。
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from model import build_lstm_model
from data_preprocessing import create_sequences
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def train_lstm_model(data, time_steps, train_size, epochs, batch_size, time_column='date'):
    # 将日期时间列分离
    time_data = data[time_column]
    data = data.drop(columns=[time_column])

    # 数据预处理
    input_scaler = MinMaxScaler()
    output_scaler = MinMaxScaler()

    # 对数值数据进行归一化
    data_scaled = input_scaler.fit_transform(data)

    # 创建训练集和测试集
    train_data = data_scaled[:int(train_size * len(data_scaled))]
    test_data = data_scaled[int(train_size * len(data_scaled)):]

    # 创建序列
    X_train, y_train = create_sequences(train_data, time_steps)
    X_test, y_test = create_sequences(test_data, time_steps)

    # 将三维数据展平为二维以便进行归一化
    num_samples_train, num_time_steps, num_features = X_train.shape
    
    # 这里假设 y_train 是二维的 (样本数, 特征数)，所以只需解包两个值
    num_samples_y_train, num_output_features = y_train.shape

    # 先 reshape 成二维
    X_train_reshaped = X_train.reshape(-1, num_features)
    y_train_reshaped = y_train.reshape(-1, num_output_features)
    X_test_reshaped = X_test.reshape(-1, num_features)
    y_test_reshaped = y_test.reshape(-1, num_output_features)

    # 对数据进行归一化
    X_train_scaled = input_scaler.fit_transform(X_train_reshaped)
    y_train_scaled = output_scaler.fit_transform(y_train_reshaped)
    X_test_scaled = input_scaler.transform(X_test_reshaped)
    y_test_scaled = output_scaler.transform(y_test_reshaped)

    # 将归一化后的数据重新转换为三维数组
    X_train_scaled = X_train_scaled.reshape(num_samples_train, num_time_steps, num_features)
    y_train_scaled = y_train_scaled.reshape(num_samples_train, num_time_steps, num_output_features)
    num_samples_test = X_test.shape[0]
    X_test_scaled = X_test_scaled.reshape(num_samples_test, num_time_steps, num_features)
    y_test_scaled = y_test_scaled.reshape(num_samples_test, num_time_steps, num_output_features)

    # 模型构建与训练
    model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))  # 确保输入形状正确
    history = model.fit(X_train_scaled, y_train_scaled, epochs=epochs, batch_size=batch_size, validation_data=(X_test_scaled, y_test_scaled))

    # 返回时，output_scaler 已经经过拟合
    return model, history, input_scaler, output_scaler, X_test_scaled, y_test_scaled
