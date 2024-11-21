# main.py
import numpy as np
import os
from itertools import product
from data_preprocessing import load_data, preprocess_data, split_data
from feature_analysis import perform_feature_analysis
from lstm_model import build_lstm_model, train_lstm_model
from visualization import plot_predictions, calculate_hit_rate, plot_with_confidence_interval
import matplotlib.pyplot as plt

# Set the correct working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load and preprocess data
filepath = "data2.csv"
data = load_data(filepath)
dates, features, scaler = preprocess_data(data)

# Split data into train and test sets
train_features, test_features = split_data(features)

# Prepare feature names (assuming the first column is 'date')
feature_names = data.columns[1:].tolist()  # Ignore the 'date' column

# Hyperparameter grid for tuning
hyperparameter_grid = {
    'lstm_units': [50, 100],  # Number of LSTM units
    'batch_size': [16, 32],   # Batch sizes
    'epochs': [30, 50],       # Number of training epochs
    'look_back': [3, 5, 7],   # Look-back windows
}

# Function to calculate bias and variance
def calculate_bias_variance(model, X_train, y_train, X_test, y_test, n_bootstraps=10):
    """
    計算 bias 和 variance
    """
    train_predictions = []
    test_predictions = []
    for _ in range(n_bootstraps):
        # Bootstrapping: 隨機抽取訓練集
        indices = np.random.choice(range(len(X_train)), len(X_train), replace=True)
        X_train_sample = X_train[indices]
        y_train_sample = y_train[indices]
        
        # 訓練模型
        model.fit(X_train_sample, y_train_sample)
        
        # 預測訓練集和測試集
        train_predictions.append(model.predict(X_train_sample))
        test_predictions.append(model.predict(X_test))

    # 計算訓練集和測試集的預測值的均值
    train_predictions = np.mean(train_predictions, axis=0)
    test_predictions = np.mean(test_predictions, axis=0)

    # 計算 bias 和 variance
    bias = np.mean((train_predictions - y_train) ** 2)
    variance = np.mean((test_predictions - np.mean(test_predictions)) ** 2)
    
    # 計算 MSE
    train_mse = np.mean((train_predictions - y_train) ** 2)
    test_mse = np.mean((test_predictions - y_test) ** 2)
    train_test_mse = train_mse/test_mse
    
    return bias, variance, train_mse, test_mse, train_test_mse
    

# Iterate over each factor for feature analysis and LSTM prediction
for target_column in range(features.shape[1]):  # Loop through all factors (columns)
    factor_name = feature_names[target_column]
    print(f"\nProcessing {factor_name}...")

    # Step 1: Perform feature importance analysis using XGBoost
    feature_importance_df = perform_feature_analysis(train_features, target_column, feature_names)
    print(f"Feature Importances for {factor_name}:\n", feature_importance_df)

    # Step 2: Hyperparameter tuning for LSTM
    best_hit_rate = -1
    best_params = {}
    best_predictions = None
    best_y_test_rescaled = None
    best_bias = None
    best_variance = None
    best_train_mse = None
    best_test_mse = None
    best_test_train = None
    best_score = 10

    # Define weight for mse and hit_rate
    weight_mse = 0.5  # Adjust this based on your preference
    weight_hit_rate = 0.5  # Adjust this based on your preference

    # Iterate through all combinations of hyperparameters
    for params in product(*hyperparameter_grid.values()):
        param_dict = dict(zip(hyperparameter_grid.keys(), params))
        print(f"Testing parameters: {param_dict}")

        # Prepare data for LSTM with current look_back
        look_back = param_dict['look_back']
        X_train, y_train = [], []
        X_test, y_test = [], []

        # Train data preparation
        for i in range(look_back, len(train_features)):
            X_train.append(train_features[i - look_back:i])
            y_train.append(train_features[i, target_column])

        # Test data preparation
        for i in range(look_back, len(test_features)):
            X_test.append(test_features[i - look_back:i])
            y_test.append(test_features[i, target_column])

        X_train, y_train = np.array(X_train), np.array(y_train)
        X_test, y_test = np.array(X_test), np.array(y_test)

        print(X_train.shape)

        # Build and train the LSTM model
        input_shape = (X_train.shape[1], X_train.shape[2])
        model = build_lstm_model(input_shape, lstm_units=param_dict['lstm_units'])
        model = train_lstm_model(
            model, 
            X_train, 
            y_train, 
            epochs=param_dict['epochs'], 
            batch_size=param_dict['batch_size'], 
            patience=5  # 提前停止的耐心次數
        )

        # Calculate Bias, Variance, and MSE
        bias, variance, train_mse, test_mse, train_test_mse = calculate_bias_variance(model, X_train, y_train, X_test, y_test)

        # Calculate hit rate
        predicted_test_values = model.predict(X_test)
        predicted_test_values_rescaled = scaler.inverse_transform(np.hstack([
            test_features[look_back:, :target_column], 
            predicted_test_values, 
            test_features[look_back:, target_column + 1:]
        ]))[:, target_column]
        y_test_rescaled = scaler.inverse_transform(np.hstack([
            test_features[look_back:, :target_column], 
            y_test.reshape(-1, 1), 
            test_features[look_back:, target_column + 1:]
        ]))[:, target_column]
        
        hit_rate, _, _ = calculate_hit_rate(y_test_rescaled, predicted_test_values_rescaled)
        print(f"Hit Rate for {factor_name} with params {param_dict}: {hit_rate:.2f}%")
        print(f"Bias: {bias:.4f}, Variance: {variance:.4f}, Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}, Test/Train: {train_test_mse:.4f}")

        # Calculate composite score (lower mse and higher hit_rate is better)
        score = weight_mse * train_test_mse + weight_hit_rate * (1 - hit_rate)

        # Save best parameters based on composite score
        if score < best_score:
            best_score = score
            best_hit_rate = hit_rate
            best_params = param_dict
            best_predictions = predicted_test_values_rescaled
            best_y_test_rescaled = y_test_rescaled
            best_bias = bias
            best_variance = variance
            best_train_mse = train_mse
            best_test_mse = test_mse
            best_test_train = train_test_mse

    # Step 6: Visualize best predictions
    dates_test = dates[-len(best_y_test_rescaled):]
    plot_predictions(dates_test, best_y_test_rescaled, best_predictions, factor_name)

    # Step 7: Visualize predictions with 95% confidence interval
    plot_with_confidence_interval(dates_test, best_y_test_rescaled, best_predictions, factor_name, train_features)

    # Output the best parameter combination and corresponding metrics
    print(f"Best Parameters for {factor_name}: {best_params}")
    print(f"Best Hit Rate for {factor_name}: {best_hit_rate:.2f}%")
    print(f"Best Bias for {factor_name}: {best_bias:.4f}")
    print(f"Best Variance for {factor_name}: {best_variance:.4f}")
    print(f"Best Train MSE for {factor_name}: {best_train_mse:.4f}")
    print(f"Best Test MSE for {factor_name}: {best_test_mse:.4f}")
    print(f"Best Test/Train MSE for {factor_name}: {best_test_train:.4f}")

     # 使用最佳參數重新訓練並驗證
    look_back = best_params['look_back']
    X_train, y_train = [], []
    X_test, y_test = [], []
    for i in range(look_back, len(train_features)):
        X_train.append(train_features[i - look_back:i])
        y_train.append(train_features[i, target_column])
    for i in range(look_back, len(test_features)):
        X_test.append(test_features[i - look_back:i])
        y_test.append(test_features[i, target_column])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_test, y_test = np.array(X_test), np.array(y_test)

    # 建立並訓練最佳模型
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]), lstm_units=best_params['lstm_units'])
    history = model.fit(X_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch_size'], validation_data=(X_test, y_test), verbose=0)

    # 繪製訓練和驗證錯誤曲線
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Train Error')
    plt.plot(history.history['val_loss'], label='Validation Error')
    plt.title(f"{factor_name} - Training and Validation Errors")
    plt.xlabel("Epochs")
    plt.ylabel("MSE")
    plt.legend()
    plt.grid()
    plt.show()