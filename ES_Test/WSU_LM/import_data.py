# import_data.py
import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

#def get_context(df, question):
 #   # Convert the question to lowercase and split it into keywords
  #  keywords = question.lower().split()
  #
 #   # Search the DataFrame for rows where the 'Abstract' contains any of the keywords
#    for keyword in keywords:
#        relevant_rows = df[df['Abstract'].str.lower().str.contains(keyword, na=False)]
#        if not relevant_rows.empty:
#            # Return the 'Abstract' of the first relevant row found
#            return relevant_rows.iloc[0]['Abstract']


def get_context(df, question):
    # Tokenize the question into keywords, ignoring common stopwords
    stopwords = set(['the', 'is', 'at', 'which', 'on', 'of', 'and', 'a', 'to'])
    keywords = [word for word in question.lower().split() if word not in stopwords]

    # Initialize variables to keep track of the best context
    best_context = ""
    max_score = 0

    # Iterate over each row in the DataFrame to find the best context
    for _, row in df.iterrows():
        # Consider both Abstract and Title for context
        content = str(row['Abstract']) + ' ' + str(row['Title'])
        score = sum(content.lower().count(keyword) for keyword in keywords)
        
        # Update the best context if the current score is higher than the max score found so far
        if score > max_score:
            best_context = f"Author: {row['Author']}. " + content
            max_score = score

    return best_context if best_context else "No relevant context found in the dataset for the question."


    return best_context
    # Default context if no match is found
    return "No relevant context found in the dataset for the question."
