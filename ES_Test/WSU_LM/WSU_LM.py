# WSU_LM.py
from import_data import load_data, get_context
from question_answering import answer_question

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def truncate_context(question, context, max_length=512):
    # Compute the maximum context length allowed (account for special tokens and question length)
    max_context_length = max_length - len(tokenizer.encode(question, add_special_tokens=True)) - 2  # -2 for [CLS] and [SEP]

    # Encode the context and truncate if necessary
    context_tokens = tokenizer.encode(context, add_special_tokens=False)
    if len(context_tokens) > max_context_length:
        context_tokens = context_tokens[:max_context_length]  # Truncate context tokens

    # Decode the truncated context tokens back to text
    truncated_context = tokenizer.decode(context_tokens, skip_special_tokens=False, clean_up_tokenization_spaces=True)
    return truncated_context




def main():
    # Load the dataset
    data_path = r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\SOARdata_merged8.csv'
    df = load_data(data_path)

    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        context = truncate_context(question, get_context(df, question))# Dynamically get context based on the dataset and question
        print("DEBUG - Using context:", context)  # Debug print to see the selected context
        
        answer = answer_question(question, context)
        print("Answer:", answer)
        print("-" * 50)


if __name__ == '__main__':
    main()
