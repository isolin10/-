#data_preprocessing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def load_data(filepath):
    data = pd.read_csv(filepath)
    data['date'] = pd.to_datetime(data['date'])
    return data

def preprocess_data(data):
    scaler = MinMaxScaler()
    features = data.iloc[:, 1:]
    scaled_features = scaler.fit_transform(features)
    return data['date'], scaled_features, scaler

def split_data(features, test_size=0.2):
    train, test = train_test_split(features, test_size=test_size, shuffle=False)
    return train, test