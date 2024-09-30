#訓練模型邏輯，包括數據加載、模型訓練和保存。
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from model import build_lstm_model
from data_preprocessing import scale_data, create_sequences, train_test_split

def train_lstm_model(data, time_steps, train_size, epochs, batch_size, time_column='date'):
    # 1. 數據處理：包含時間列時處理時間轉換
    scaled_data, scaler = scale_data(data, time_column)
    train_data, test_data = train_test_split(scaled_data, train_size)
    
    # 2. 創建時間序列
    X_train, y_train = create_sequences(train_data, time_steps)
    X_test, y_test = create_sequences(test_data, time_steps)
    
    # 3. 構建模型
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    
    # 4. 模型訓練
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_test, y_test), callbacks=[early_stopping])

    # 5. 模型保存
    model.save('lstm_model.h5')
    
    return model, history, scaler
