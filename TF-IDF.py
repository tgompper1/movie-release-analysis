import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
#install pandas and scikit-learn before run the code
#by using pip install pandas/scikit-learn in command line


# Load the dataset
file_path_all_data = 'E:\Comp370\movie_annotation.tsv'  # Replace with the path to your file
all_data = pd.read_csv(file_path_all_data, sep='\t')

# Combine 'title' and 'description' into a single text document
all_data['text'] = all_data['title'] + ' ' + all_data['description']

# Preprocess the text
all_data['text'] = all_data['text'].str.lower()
all_data['text'] = all_data['text'].str.replace('[^\w\s]', '')  # Remove punctuation
all_data['text'] = all_data['text'].str.replace('\d+', '')  # Remove numbers

# Group the text by 'annotation' (category)
grouped_text = all_data.groupby('annotation')['text'].apply(' '.join)

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)

# Fit the vectorizer and transform the grouped text data
tfidf_matrix = tfidf_vectorizer.fit_transform(grouped_text)

# Get feature names (words)
feature_names = np.array(tfidf_vectorizer.get_feature_names_out())

# Function to get top n TF-IDF values in row and return them with their corresponding feature names
def top_tfidf_feats(row, features, top_n=10):
    sorted_indices = np.argsort(row)[::-1]
    top_features = [(features[i], row[i]) for i in sorted_indices[:top_n]]
    return top_features

# Calculate top 10 words for each category
top_words = {}
for category in grouped_text.index:
    row_id = grouped_text.index.get_loc(category)
    row = np.squeeze(tfidf_matrix[row_id].toarray())
    top_words[category] = top_tfidf_feats(row, feature_names, 10)

# Display top words for each category
for category, words in top_words.items():
    print(f"{category.capitalize()}:")
    for word, score in words:
        print(f" - {word}: {score:.2f}")
    print("\n")
