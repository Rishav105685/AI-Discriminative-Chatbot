import random
import json
from collections import Counter
from nltk.stem import WordNetLemmatizer
import numpy as np

# Function to preprocess text data (lowercase, remove punctuation, stemming)
def preprocess_text(text):
    import string
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    from nltk.stem.porter import PorterStemmer
    stemmer = PorterStemmer()
    words = text.split()
    words = [stemmer.stem(word) for word in words]
    return words

# Function to load book data from JSON file
def load_books(data_path):
    with open(data_path, "r") as f:
        books = json.load(f)
    return books

# Function to create vocabulary from keywords and descriptions
def create_vocabulary(books):
    vocabulary = set()
    for book in books:
        keywords = preprocess_text(book["keywords"])
        description = preprocess_text(book["description"])
        vocabulary.update(keywords)
        vocabulary.update(description)
    return vocabulary

# Function to create bag-of-words representation for queries and books
def bag_of_words(text, vocabulary):
    bag = [0] * len(vocabulary)
    for word in preprocess_text(text):
        if word in vocabulary:
            bag[vocabulary.index(word)] = 1
    return np.array(bag)

# Function to calculate cosine similarity between two bag-of-words vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Main program flow
def main():
    # Load book data from JSON file (replace with your data path)
    data_path = "intents.json"
    books = load_books(data_path)

    # Create vocabulary from keywords and descriptions
    vocabulary = create_vocabulary(books)

    # User input loop
    while True:
        user_query = input("Enter keywords or phrases related to books you're interested in: ")

        # Create bag-of-words representation for user query
        user_query_bow = bag_of_words(user_query, vocabulary)

        # Calculate similarity scores between user query and each book
        similarity_scores = []
        for book in books:
            description_bow = bag_of_words(book["description"], vocabulary)
            similarity = cosine_similarity(user_query_bow, description_bow)
            similarity_scores.append((book, similarity))

        # Sort recommendations by similarity score (descending)
        sorted_recommendations = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Present top 5 recommendations
        print("Here are some book recommendations for you:")
        for i, (book, score) in enumerate(sorted_recommendations[:5]):
            print(f"- {book['name']} by {book.get('author', 'Unknown')}")
            print(f"\tSimilarity Score: {score:.2f}")

        # Optionally, consider adding more refined recommendations based on keywords
        # You can analyze user query keywords and identify relevant books based on keyword presence

if __name__ == "__main__":
    main()
