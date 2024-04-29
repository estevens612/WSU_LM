import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def load_data():
    data = pd.read_csv(r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\SOARdata_merged2.csv')
    data['combined_text'] = data['Title'].fillna('') + " " + data['Abstract'].fillna('')
    data['combined_text'] = data['combined_text'].apply(preprocess_text)
    vectorizer = TfidfVectorizer()
    text_vectors = vectorizer.fit_transform(data['combined_text'])
    return data, vectorizer, text_vectors

def search_database(query, data, vectorizer, text_vectors, num_matches=10):
    query_vector = vectorizer.transform([preprocess_text(query)])
    similarity_scores = cosine_similarity(query_vector, text_vectors).flatten()
    
    top_n_indices = np.argpartition(similarity_scores, -num_matches)[-num_matches:]
    top_n_indices = top_n_indices[np.argsort(similarity_scores[top_n_indices])[::-1]]

    results = []
    for index in top_n_indices:
        author = data.iloc[index]['Author']
        title = data.iloc[index]['Title']
        email = "example@wichita.com"
        phone = "(555)123-4567"
        website = f"{author.replace(' ', '')}.com"
        result = (f"Author: {author}\nTitle: {title}\nEmail: {email}\nPhone Number: {phone}\n"
                  f"Personal website: {website}\n{'-' * 40}\n")
        results.append(result)
    return results
