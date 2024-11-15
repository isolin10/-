#lstm_model.py

from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np



def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        LSTM(50, return_sequences=False),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm_model(model, train_data, train_target, epochs=50, batch_size=32):
    train_data = np.array(train_data)
    train_target = np.array(train_target)
    model.fit(train_data, train_target, epochs=epochs, batch_size=batch_size)
    return model
