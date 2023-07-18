import json
import numpy as np
from datetime import datetime, timedelta
from GenerateDataUtils import get_event_per_day, align_dates_of_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from GenerateDataSets import getData
#alternativ repository issuePath='../Main/next.js_vercel_issues.json', commitPath='../Main/next.js_vercel_commits.json'
# Call the getData function and get the data
dates, commit_counts, issue_labels = getData(issuePath='../Main/next.js_vercel_issues.json', commitPath='../Main/next.js_vercel_commits.json')

# Convert the datetime.date objects to numeric values (days since a reference date)
dates_numeric = [(date - min(dates)).days for date in dates]

# Normalize commit_counts and dates_numeric between 0 and 1
scaler = MinMaxScaler()
commit_counts = scaler.fit_transform(np.array(commit_counts).reshape(-1, 1)).flatten()
dates_numeric = scaler.fit_transform(np.array(dates_numeric).reshape(-1, 1)).flatten()

# Split the data into training and testing datasets (80% for training, 20% for testing)
dates_train, dates_test, commit_counts_train, commit_counts_test, issue_labels_train, issue_labels_test = train_test_split(
    dates_numeric, commit_counts, issue_labels, test_size=0.2, random_state=42)

# Build the TensorFlow model
model = Sequential([
    Dense(128, activation='relu', input_shape=(2,)),  # Two features: commit count and days since reference date
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
Dense(32, activation='sigmoid'),
    Dense(1, activation='sigmoid')  # Output layer with sigmoid activation for binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Prepare the input data for training
input_data_train = np.column_stack((commit_counts_train, dates_train))

# Train the model on the training data
model.fit(input_data_train, issue_labels_train, epochs=10, batch_size=32)

# Prepare the input data for testing
input_data_test = np.column_stack((commit_counts_test, dates_test))

# Evaluate the model on the test data
loss, accuracy = model.evaluate(input_data_test, issue_labels_test)
print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")
model.save("my_trained_model_binary.h5")