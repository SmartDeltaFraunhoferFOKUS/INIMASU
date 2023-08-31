import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download('stopwords')

# Process and clean up labels
def process_labels(labels):
    for i in range(len(labels)):
        if type(labels[i]) == list:
            new_label = check_entry(labels[i])
            labels[i] = new_label
    return labels

# Process and clean up description
def process_description(description):
    for i in range(len(description)):
        entry = description[i]
        if type(entry) == list:
            entry = ", ".join(list(filter(lambda x: x != 0, entry)))
            # Check if the entry only consists of 0
            if entry:
                description[i] = clean_up_string(entry)
            else:
                description[i] = 0
    return description

# Check and clean up an entry
def check_entry(entry):
    # Get rid of 0
    entry = list(filter(lambda x: x != 0, entry))

    # Boolean to check if there is information in the entry
    has_label_str = False

    # Look for entries with information
    for i in range(len(entry)):
        value = entry[i]
        if type(value) == list:
            # Reduce complexity of entry
            entry[i] = clean_up_string(list_of_dic_to_string(entry[i]))
            has_label_str = True

    # Bring information into a string
    if has_label_str:
        entry = ", ".join(entry)
        return entry
    else:
        return 0

# Convert a list of dictionaries to a string
def list_of_dic_to_string(data):
    dict_strings = [' , '.join([f"{key}: {value}" for key, value in item.items()]) for item in data]

    delimiter = ' , '

    # Use join() to concatenate the list of dictionary strings
    result_string = delimiter.join(dict_strings)
    return result_string

# Clean up and preprocess a string
def clean_up_string(text):
    stemmer = PorterStemmer()

    stop_words = set(stopwords.words('english'))

    # Remove URLs and non-alphanumeric characters
    text = re.sub(r'https?:\/\/[^\s]*', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Tokenize the text into words
    words = text.split()

    # Remove stop words
    #custom_stop_words = ['id', 'node_id', "name", "description", "url", "default", "color"]
    #stop_words.update(custom_stop_words)
    words = [word for word in words if word not in stop_words]

    # Stem the words
    words = [stemmer.stem(word) for word in words]

    # Join the preprocessed words back into a string
    preprocessed_text = ' '.join(words)

    return preprocessed_text
