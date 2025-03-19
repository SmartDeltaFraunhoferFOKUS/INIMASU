import os
import numpy as np
from keras.layers import Dropout
from keras_preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from IssuePredictionAI.GenerateDataSets.GenerateDataSets import getData
from IssuePredictionAI.GenerateDataSets.GenerateDataUtils import generate_input_sequences, generate_label_sequences

# when is he predict window going to start
n_days_prediction = 1
# number of days, that the modell can learn and predict from
analysis_window = 10
# time frame that the model predicts
predict_window = 7

# Call the getData function and get the data
dates, commit_counts, issue_labels, added, subtracted, new_release = getData(numberIssues=True)

# Shift issue labels by n_days_prediction
issue_labels_shifted = np.array(issue_labels[n_days_prediction:])

# Remove the last n_days_prediction elements from commit_counts and dates
commit_counts = np.array(commit_counts[:-n_days_prediction ])
dates = np.array(dates[:-n_days_prediction])
added = np.array(added[:-n_days_prediction])
new_release = np.array(new_release[:-n_days_prediction ])
subtracted = np.array(subtracted[:-n_days_prediction])

# Convert the datetime.date objects to numeric values (days since a reference date)
dates_numeric = [(date - min(dates)).days for date in dates]

# Prepare the input data for training
input_data_train = np.column_stack((commit_counts, dates_numeric, added, subtracted, new_release))

# Normalize the input features using StandardScaler
scaler = StandardScaler()
input_data_train = scaler.fit_transform(input_data_train)


input_sequences = generate_input_sequences(input_data_train, predict_window, analysis_window, f'input_sequences_train_{n_days_prediction}_{predict_window}_{analysis_window}.npy')
issue_labels_shifted_rolling_window = generate_label_sequences(issue_labels_shifted, predict_window, analysis_window,f'input_sequences_label_{n_days_prediction}_{predict_window}_{analysis_window}.npy' )

# Split the data into training and testing datasets
input_train, input_test, issue_labels_train, issue_labels_test = train_test_split(
    input_sequences, issue_labels_shifted_rolling_window, test_size=0.2, random_state=42)





# Build the TensorFlow model
model = Sequential([
    Dense(512, activation='relu', input_shape=(input_train.shape[1],)),
    Dropout(0.4),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(predict_window, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Train the model on the training data
model.fit(input_train, issue_labels_train, epochs=20, batch_size=64)

# Evaluate the model on the test data
loss, mean_absolute_error = model.evaluate(input_test, issue_labels_test)
print(f"Test loss: {loss:.4f}, Test mean_absolute_error: {mean_absolute_error:.4f}")

# Save the model
model.save("my_trained_model.h5")
