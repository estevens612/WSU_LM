# WSU_LM.py
from import_data import load_data, get_context
from question_answering import answer_question

def main():
    # Load the dataset
    data_path = r'C:\Users\estev\Desktop\WSU_LM\ES_Test\WSU_LM\SOARdata_merged2.csv'
    df = load_data(data_path)

    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        context = get_context(df, question)  # Dynamically get context based on the dataset and question
        print("DEBUG - Using context:", context)  # Debug print to see the selected context
        
        answer = answer_question(question, context)
        print("Answer:", answer)
        print("-" * 50)


if __name__ == '__main__':
    main()
