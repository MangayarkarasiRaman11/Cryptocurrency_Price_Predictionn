from keras.models import Sequential
from keras.layers import Dense, Input
import numpy as np


def gen_main(data, seed=123):
    np.random.seed(seed)

    if len(data) == 0:
        print("Error: No data available for training.")
        return []

    # Prepare training data
    x_data = np.array(range(len(data), 0, -1))
    y_data = np.array(data)

    # Define model
    model = Sequential([
        Input(shape=(1,)),  # Use Input layer
        Dense(10, activation='relu'),
        Dense(10, activation='relu'),
        Dense(10, activation='relu'),
        Dense(1, activation='linear')  # Use linear activation for regression
    ])

    model.compile(loss="mean_squared_error", optimizer="adam")

    # Train model
    model.fit(x_data, y_data, epochs=500, batch_size=10, verbose=0)

    # Make predictions
    predictions = model.predict(x_data)

    return predictions.flatten()
