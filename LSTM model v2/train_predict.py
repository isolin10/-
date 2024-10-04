#訓練與預測
# train_predict.py
from keras.models import Sequential
from lstm_model import build_lstm_model
from sklearn.model_selection import GridSearchCV, KFold
from keras.layers import LSTM, Dense, Dropout
from keras.wrappers.scikit_learn import KerasRegressor

def create_model(optimizer='adam', dropout_rate=0.2, input_shape=(10, 8)):  # 假設特徵數量為8
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(50))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

def train_and_predict_with_grid_search(X_train, y_train, X_test, scaler):
    model = KerasRegressor(build_fn=create_model, verbose=0)
    
    # 定義參數範圍
    param_grid = {
        'batch_size': [16, 32, 64],
        'epochs': [50, 100],
        'optimizer': ['adam', 'rmsprop'],
        'dropout_rate': [0.2, 0.3],
        'input_shape': [(X_train.shape[1], X_train.shape[2])]  # 這裡動態獲取輸入形狀
    }
    
    # 進行網格搜索
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)
    grid_result = grid.fit(X_train, y_train)
    
    # 最佳參數
    print(f"Best parameters: {grid_result.best_params_}")
    
    # 使用最佳模型進行預測
    best_model = grid_result.best_estimator_
    y_pred_scaled = best_model.predict(X_test)

    # 反標準化
    y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))
    
    return y_pred, grid_result.best_params_
