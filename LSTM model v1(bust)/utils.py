#一些通用的工具函數，比如畫圖和模型評估。
import matplotlib.pyplot as plt
import os

# 設定正確的工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def plot_loss(history):
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

def evaluate_model(model, X_test, y_test, output_scaler):
    # 预测
    predictions = model.predict(X_test)

    # 获取测试集的样本数量
    num_samples_test = y_test.shape[0]

    # 将 y_test 和 predictions 都从三维变为二维，以便进行反归一化
    y_test_reshaped = y_test.reshape(-1, y_test.shape[-1])
    predictions_reshaped = predictions.reshape(-1, predictions.shape[-1])

    # 进行反归一化
    y_test_rescaled = output_scaler.inverse_transform(y_test_reshaped)
    predictions_rescaled = output_scaler.inverse_transform(predictions_reshaped)

    # 重新将反归一化后的数据变为三维
    y_test_rescaled = y_test_rescaled.reshape(num_samples_test, -1, y_test.shape[-1])
    predictions_rescaled = predictions_rescaled.reshape(num_samples_test, -1, predictions.shape[-1])

    return predictions_rescaled, y_test_rescaled
