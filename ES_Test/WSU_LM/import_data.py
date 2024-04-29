# import_data.py
import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def get_context(df, question):
    stopwords = set(['the', 'is', 'at', 'which', 'on', 'of', 'and', 'a', 'to'])
    keywords = [word for word in question.lower().split() if word not in stopwords]

    def score_row(row):
        content = str(row['Abstract']) + ' ' + str(row['Title'])
        return sum(content.lower().count(keyword) for keyword in keywords)

    df['score'] = df.apply(score_row, axis=1)
    best_row = df.loc[df['score'].idxmax()] if not df.empty else None

    if best_row is not None and best_row['score'] > 0:
        return f"Author: {best_row['Author']}. {best_row['Abstract']} {best_row['Title']}"
    else:
        return "No relevant context found in the dataset for the question."
