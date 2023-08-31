import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from IssuePredictionAI.GenerateDataSets.GenerateDataSets import getData

# Alternative repository issuePath='../Main/next.js_vercel_issues.json', commitPath='../Main/next.js_vercel_commits.json'

n_days_prediction = 1

# Call the getData function and get the data
dates, commit_counts, issue_labels, added, subtracted, new_release = getData(numberIssues=True)

# Shift issue labels by n_days_prediction
issue_labels_shifted = np.array(issue_labels[n_days_prediction:])
# Remove the last n_days_prediction elements from commit_counts and dates
commit_counts = np.array(commit_counts[:-n_days_prediction])
dates = np.array(dates[:-n_days_prediction])
added = np.array(added[:-n_days_prediction])
new_release = np.array(new_release[:-n_days_prediction])

subtracted = np.array(subtracted[:-n_days_prediction])

# Convert the datetime.date objects to numeric values (days since a reference date)
dates_numeric = [(date - min(dates)).days for date in dates]

# Prepare the input data for training
input_data_train = np.column_stack((commit_counts, dates_numeric, added, subtracted, new_release))

# Split the data into training and testing datasets (80% for training, 20% for testing)
input_train, input_test, issue_labels_train, issue_labels_test = train_test_split(
    input_data_train, issue_labels_shifted, test_size=0.2, random_state=42)

# Build the TensorFlow model
model = Sequential([
    Dense(512, activation='relu', input_shape=(input_train.shape[1],)),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Train the model on the training data
model.fit(input_train, issue_labels_train, epochs=50, batch_size=64)

# Evaluate the model on the test data
loss, mean_absolute_error = model.evaluate(input_test, issue_labels_test)
print(f"Test loss: {loss:.4f}, Test mean_absolute_error: {mean_absolute_error:.4f}")

# Save the model
model.save("my_trained_model.h5")
