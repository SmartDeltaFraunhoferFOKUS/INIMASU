import numpy as np
from keras import Model
from keras.layers import Input, Concatenate, Dense, Dropout
from keras.saving.save import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from IssuePredictionAI.GenerateDataSets.AnalyzeTextImportency import analyze_feature_importance, \
    calculate_feature_importance
from IssuePredictionAI.GenerateDataSets.GenerateDataUtils import vectorizing_own_model
from IssuePredictionAI.GenerateDataSets.GenerateDataSets import getData

n_days_prediction = 1

# Get the data
data = getData(textVectorization=True)
dates, commit_counts, issue_counts, vec_labels_issues, vec_description_issue, vec_message_commit, added, subtracted = data

# Vectorize text features
vec_labels_issues_int, vec_labels_issues_layer = vectorizing_own_model(vec_labels_issues, giveLayer=True, vocab_size=2800)
vec_description_issue_int, vec_description_issue_layer = vectorizing_own_model(vec_description_issue, giveLayer=True, vocab_size=100)
vec_message_commit_int, vec_message_commit_layer  = vectorizing_own_model(vec_message_commit, giveLayer=True, vocab_size=500)

# Convert dates to numeric values
dates_numeric = [(date - min(dates)).days for date in dates]

# Prepare data for prediction
issue_counts = np.array(issue_counts[n_days_prediction:])
commit_counts = np.array(commit_counts[:-n_days_prediction])
dates_numeric = np.array(dates_numeric[:-n_days_prediction])
added = np.array(added[:-n_days_prediction])
subtracted = np.array(subtracted[:-n_days_prediction])

# Stack the vectorized data
vec_labels_issues = np.array(vec_labels_issues_int)[:-n_days_prediction]
vec_description_issue = np.array(vec_description_issue_int)[:-n_days_prediction]
vec_message_commit = np.array(vec_message_commit_int)[:-n_days_prediction]

# Concatenate input data
input_data = np.column_stack((
    dates_numeric, commit_counts, vec_labels_issues,
    vec_description_issue, vec_message_commit, added, subtracted
))

# Split data
input_data_train, input_data_test, issue_counts_train, issue_counts_test, added_train, added_test, subtracted_train, subtracted_test = train_test_split(
    input_data, issue_counts, added, subtracted, test_size=0.2, random_state=42
)

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Fit and transform the scaler on your input data
input_data_train_normalized = scaler.fit_transform(input_data_train)
input_data_test_normalized = scaler.transform(input_data_test)






# Define input shapes
input_shape_vec_labels_issues = (vec_labels_issues.shape[1],)
input_shape_vec_description_issue = (vec_description_issue.shape[1],)
input_shape_vec_message_commit = (vec_message_commit.shape[1],)

# Define input layers
input_dates = Input(shape=(1,), name='input_dates')
input_commit_counts = Input(shape=(1,), name='input_commit_counts')
input_vec_labels_issues = Input(shape=input_shape_vec_labels_issues, name='input_vec_labels_issues')
input_vec_description_issue = Input(shape=input_shape_vec_description_issue, name='input_vec_description_issue')
input_vec_message_commit = Input(shape=input_shape_vec_message_commit, name='input_vec_message_commit')
input_added = Input(shape=(1,), name='input_added')
input_subtracted = Input(shape=(1,), name='input_subtracted')

# Define dense layers
dense_dates = Dense(128, activation='relu')(input_dates)
dense_commit_counts = Dense(128, activation='relu')(input_commit_counts)
dense_vec_labels_issues = Dense(128, activation='relu')(input_vec_labels_issues)
dense_vec_description_issue = Dense(64, activation='relu')(input_vec_description_issue)
dense_vec_message_commit = Dense(128, activation='relu')(input_vec_message_commit)
dense_added = Dense(64, activation='relu')(input_added)
dense_subtracted = Dense(64, activation='relu')(input_subtracted)

# Concatenate inputs
concatenated = Concatenate()([
    dense_dates, dense_commit_counts, dense_vec_labels_issues,
    dense_vec_description_issue, dense_vec_message_commit,
    dense_added, dense_subtracted
])

# Dense layers
dense1 = Dense(512, activation='relu')(concatenated)
dropout1 = Dropout(0.3)(dense1)
dense2 = Dense(256, activation='relu')(dense1)
dense3 = Dense(64, activation='relu')(dense2)
output_layer = Dense(1, activation='linear')(dense3)

# Prepare input data
input_data_train_dict = {
    'input_dates': input_data_train[:, [0]],
    'input_commit_counts': input_data_train[:, [1]],
    'input_vec_labels_issues': input_data_train[:, 2:2 + input_shape_vec_labels_issues[0]],
    'input_vec_description_issue': input_data_train[:, 2 + input_shape_vec_labels_issues[0]:2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0]],
    'input_vec_message_commit': input_data_train[:, 2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0]:2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0] + input_shape_vec_message_commit[0]],
    'input_added': added_train,
    'input_subtracted': subtracted_train
}

# Prepare input data
input_data_test_dict = {
    'input_dates': input_data_test[:, [0]],
    'input_commit_counts': input_data_test[:, [1]],
    'input_vec_labels_issues': input_data_test[:, 2:2 + input_shape_vec_labels_issues[0]],
    'input_vec_description_issue': input_data_test[:, 2 + input_shape_vec_labels_issues[0]:2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0]],
    'input_vec_message_commit': input_data_test[:, 2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0]:2 + input_shape_vec_labels_issues[0] + input_shape_vec_description_issue[0] + input_shape_vec_message_commit[0]],
    'input_added': added_test,
    'input_subtracted': subtracted_test
}


model = Model(inputs=[
    input_dates, input_commit_counts, input_vec_labels_issues,
    input_vec_description_issue, input_vec_message_commit,
    input_added, input_subtracted
], outputs=output_layer)

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Train the model
model.fit(
    input_data_train_dict,
    issue_counts_train,
    epochs=15,
    batch_size=128
)

# Evaluate the model
loss, mae = model.evaluate(
    input_data_test_dict,
    issue_counts_test,
    verbose=0
)

# Print the evaluation results
print(f"Test loss: {loss:.4f}, Test MAE: {mae:.4f}")


# Save the model
model.save("my_trained_model_amount_strings.h5")



