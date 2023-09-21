def analyze_feature_importance(vocabularies, model, feature_importance, top_n=10):
    """
    Analyze feature importance scores and map them to vocabulary words or tokens.
    Also, identify and store unimportant features for each vocabulary.

    Args:
        vocabularies (list of list): A list of lists containing words or tokens for each vocabulary.
        model (keras.Model): The trained Keras model.
        feature_importance (numpy.ndarray): Importance scores for each feature (neuron).
        top_n (int): Number of top features to analyze.

    Returns:
        dict: A dictionary containing both important and unimportant features for each vocabulary.
    """
    # Create a mapping between neuron indices and vocabulary indices for each vocabulary
    neuron_to_vocab_mapping = {}  # Maps neuron index to vocabulary index for each vocabulary
    for vocab_index, vocab in enumerate(vocabularies):
        vocab_mapping = {}
        for i, word in enumerate(vocab):
            vocab_mapping[i] = word
        neuron_to_vocab_mapping[vocab_index] = vocab_mapping

    # Sort features by importance in descending order
    sorted_features = sorted(enumerate(feature_importance), key=lambda x: -x[1])

    # Prepare the list of top features and unimportant features for each vocabulary
    top_features = {}
    unimportant_features = {}

    # Analyze the top N important features for each vocabulary
    for vocab_index, vocab in enumerate(vocabularies):
        top_features[vocab_index] = []
        unimportant_features[vocab_index] = []

    for i in range(top_n):
        feature_index, importance_score = sorted_features[i]
        for vocab_index, vocab in enumerate(vocabularies):
            vocab_mapping = neuron_to_vocab_mapping[vocab_index]
            feature_word = vocab_mapping.get(feature_index, "Unknown")  # Get the corresponding word

            # Collect feature details in a dictionary
            feature_details = {
                "Feature Index": feature_index,
                "Word or Token": feature_word,
                "Importance Score": importance_score
            }

            top_features[vocab_index].append(feature_details)

    # Identify unimportant features for each vocabulary
    for i in range(top_n, len(sorted_features)):
        feature_index, importance_score = sorted_features[i]
        for vocab_index, vocab in enumerate(vocabularies):
            vocab_mapping = neuron_to_vocab_mapping[vocab_index]
            feature_word = vocab_mapping.get(feature_index, "Unknown")  # Get the corresponding word

            # Collect feature details in a dictionary
            feature_details = {
                "Feature Index": feature_index,
                "Word or Token": feature_word,
                "Importance Score": importance_score
            }

            unimportant_features[vocab_index].append(feature_details)

    return {"important_features": top_features, "unimportant_features": unimportant_features}

import numpy as np
from sklearn.inspection import permutation_importance

def calculate_feature_importance(model, X, y, scoring_metric='accuracy', n_repeats=10, random_state=None):
    """
    Calculate feature importance using permutation importance.

    Args:
        model (object): A trained machine learning model (e.g., Keras Model).
        X (numpy.ndarray): Input features (shape: [n_samples, n_features]).
        y (numpy.ndarray): Target labels (shape: [n_samples]).
        scoring_metric (str): Scoring metric for evaluating feature importance (e.g., 'accuracy', 'r2', 'neg_mean_squared_error').
        n_repeats (int): Number of times to repeat the permutation process for more reliable results.
        random_state (int or None): Random seed for reproducibility.

    Returns:
        sklearn.inspection.permutation_importance: PermutationImportance object containing feature importances.
    """
    # Perform permutation importance calculation
    perm_importance = permutation_importance(
        model, X, y, scoring=scoring_metric, n_repeats=n_repeats, random_state=random_state
    )
    return perm_importance

# Example usage:
# Replace 'your_model', 'your_X', and 'your_y' with your actual model, input features, and target labels
# Replace 'your_scoring_metric' with an appropriate scoring metric for your problem (e.g., 'accuracy', 'r2', 'neg_mean_squared_error')

# feature_importance = calculate_feature_importance(your_model, your_X, your_y, scoring_metric=your_scoring_metric)
