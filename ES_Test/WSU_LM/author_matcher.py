import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def preprocess_text(text):
    # Basic preprocessing to remove punctuation and lowercase the text
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    return text

def main():
    # Load the dataset
    data = pd.read_csv(r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\SOARdata_merged2.csv')
    
    # Combine title and abstract and preprocess
    data['combined_text'] = data['Title'].fillna('') + " " + data['Abstract'].fillna('')
    data['combined_text'] = data['combined_text'].apply(preprocess_text)
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    text_vectors = vectorizer.fit_transform(data['combined_text'])
    
    # User query input loop
    while True:
        query = input("Enter your search query about research topics (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        query_vector = vectorizer.transform([preprocess_text(query)])
        similarity_scores = cosine_similarity(query_vector, text_vectors)
        best_match_index = similarity_scores.argmax()
        best_match_author = data.iloc[best_match_index]['Author']
        best_match_title = data.iloc[best_match_index]['Title']

        print(f"Best match author: {best_match_author}")
        print(f"Associated Title: {best_match_title}")

if __name__ == "__main__":
    main()
