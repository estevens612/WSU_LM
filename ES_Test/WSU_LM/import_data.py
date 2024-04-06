# import_data.py
import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def get_context(df, question):
    # Convert the question to lowercase and split it into keywords
    keywords = question.lower().split()

    # Search the DataFrame for rows where the 'Abstract' contains any of the keywords
    for keyword in keywords:
        relevant_rows = df[df['Abstract'].str.lower().str.contains(keyword, na=False)]
        if not relevant_rows.empty:
            # Return the 'Abstract' of the first relevant row found
            return relevant_rows.iloc[0]['Abstract']

    # Default context if no match is found
    return "No relevant context found in the dataset for the question."
