#main.py

import numpy as np
import os
from data_preprocessing import load_data, preprocess_data, split_data
from feature_analysis import perform_feature_analysis
from lstm_model import build_lstm_model, train_lstm_model
from visualization import plot_predictions, calculate_hit_rate, plot_with_confidence_interval

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

# Iterate over each factor for feature analysis and LSTM prediction
for target_column in range(features.shape[1]):  # Loop through all factors (columns)
    factor_name = feature_names[target_column]
    print(f"\nProcessing {factor_name}...")

    # Step 1: Perform feature importance analysis using XGBoost
    feature_importance_df = perform_feature_analysis(train_features, target_column, feature_names)
    print(f"Feature Importances for {factor_name}:\n", feature_importance_df)

    # Step 2: Prepare data for LSTM
    look_back = 5
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

    # Step 3: Build and train the LSTM model
    input_shape = (X_train.shape[1], X_train.shape[2])
    model = build_lstm_model(input_shape)
    model = train_lstm_model(model, X_train, y_train)

    # Step 4: Make predictions
    predicted_test_values = model.predict(X_test)

    # Step 5: Reverse scaling of predictions to original scale
    predicted_test_values_rescaled = scaler.inverse_transform(np.hstack([test_features[look_back:, :target_column], predicted_test_values, test_features[look_back:, target_column + 1:]]))[:, target_column]
    y_test_rescaled = scaler.inverse_transform(np.hstack([test_features[look_back:, :target_column], y_test.reshape(-1, 1), test_features[look_back:, target_column + 1:]]))[:, target_column]

    # Step 6: Visualize predictions
    dates_test = dates[-len(y_test):]
    plot_predictions(dates_test, y_test_rescaled, predicted_test_values_rescaled, factor_name)

    # Step 7: Calculate hit rate
    hit_rate, lower_bound, upper_bound = calculate_hit_rate(y_test_rescaled, predicted_test_values_rescaled)
    print(f"Hit Rate for {factor_name}: {hit_rate:.2f}%")
    print(f"95% Confidence Interval for {factor_name}: [{lower_bound:.2f}, {upper_bound:.2f}]")

    # Step 8: Plot with confidence interval
    plot_with_confidence_interval(dates_test, y_test_rescaled, predicted_test_values_rescaled, factor_name, train_features)
