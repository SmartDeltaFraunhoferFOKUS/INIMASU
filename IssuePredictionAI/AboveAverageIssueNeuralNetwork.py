import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # Import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from IssuePredictionAI.GenerateDataSets.GenerateDataSets import getData

# Alternative repository issuePath='../Main/next.js_vercel_issues.json', commitPath='../Main/next.js_vercel_commits.json'

n_days_prediction = 1

# Call the getData function and get the data
dates, commit_counts, issue_counts, added, subtracted, new_release = getData()

# Shift issue labels by n_days_prediction
issue_labels_shifted = issue_counts[n_days_prediction:]
# Remove the last n_days_prediction elements from commit_counts and dates
commit_counts = commit_counts[:-n_days_prediction]
dates = dates[:-n_days_prediction]
added = np.array(added[:-n_days_prediction])
new_release = np.array(new_release[:-n_days_prediction])
subtracted = np.array(subtracted[:-n_days_prediction])

# Convert the datetime.date objects to numeric values (days since a reference date)
dates_numeric = [(date - min(dates)).days for date in dates]

# Feature Engineering: You can add a new feature, such as the product of 'added' and 'subtracted'.
input_data = np.column_stack((commit_counts, dates_numeric, added, subtracted, new_release))

# Normalize the input data using StandardScaler
scaler = StandardScaler()
input_data = scaler.fit_transform(input_data)

# Split the data into training and testing datasets (80% for training, 20% for testing)
input_train, input_test, issue_labels_train, issue_labels_test = train_test_split(
    input_data, issue_labels_shifted, test_size=0.2, random_state=42)

# Build the TensorFlow model with dropout layers for regularization.
model = keras.Sequential([
    layers.Dense(512, activation='relu', input_shape=(5,)),
    layers.Dropout(0.5),  # Dropout layer for regularization
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.1),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model with appropriate loss and metrics
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the training data
history = model.fit(input_train, issue_labels_train, epochs=20, batch_size=32, validation_split=0.2)

# Evaluate the model on the test data
loss, accuracy = model.evaluate(input_test, issue_labels_test)
print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

# Save the model
model.save("my_trained_model.h5")

# Ensemble Learning (Random Forest)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(input_train, issue_labels_train)

# Evaluate the Random Forest classifier
rf_predictions = rf_classifier.predict(input_test)
rf_accuracy = accuracy_score(issue_labels_test, rf_predictions)
print(f"Random Forest Accuracy: {rf_accuracy:.4f}")

# Feature Importance Analysis (Using Permutation Importance)
perm_importance = permutation_importance(rf_classifier, input_test, issue_labels_test, n_repeats=30, random_state=42)
# Display feature importances
for i, imp in enumerate(perm_importance.importances_mean):
    print(f"Feature {i + 1}: {imp:.4f}")
