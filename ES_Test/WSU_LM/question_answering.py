# question_answering.py
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from BERT_Core import tokenizer, model  # Import tokenizer and model from BERT_Core.py

def answer_question(question, context):
    # Tokenization and model processing as before
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    # Find start and end tokens for the answer
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1

    # Decode the answer, ensuring it starts with the author's name
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][answer_start:answer_end]))

    return answer

