import pandas as pd
import json

# Load the dataset
data = pd.read_csv(r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\SOARdata_merged2.csv')

entries = []
for index, row in data.iterrows():
    if pd.notna(row['Abstract']) and pd.notna(row['Author']):
        context = f"{row['Title']}. {row['Abstract']}"
        question = "Who is the author discussed in this context?"
        answer_text = row['Author']
        answer_start = context.find(answer_text)

        if answer_start != -1:  # Check if the answer is found in the context
            entry = {
                "context": context,
                "question": question,
                "answers": {
                    "text": [answer_text],  # List format to support multiple correct answers
                    "answer_start": [answer_start]
                }
            }
            entries.append(entry)
        else:
            print("Answer not found in context:", row['Author'])  # Debugging output
    else:
        print("Missing data in row:", index)  # Debugging output

# Save to JSON file
with open(r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\question_answering_data.json', 'w') as f:
    json.dump(entries, f, indent=4)

print("JSON file created with {} entries.".format(len(entries)))
