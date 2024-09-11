from conversation_extractor import fetch_conversation_from_link
from vector_store import process_and_store_conversation
from rag_retrieve import retrieve_and_generate

def export_and_store_conversation(conversation_link):

    conversation_data = fetch_conversation_from_link(conversation_link)
    if conversation_data:

        vectorstore = process_and_store_conversation(conversation_data)
        return vectorstore
    else:
        print("대화 내용을 변환하지 못했습니다.")
        return None


if __name__ == "__main__":
    link = "https://chatgpt.com/share/657832e7-1c82-4aac-8ee3-75a55188c26c" 

    vectorstore = export_and_store_conversation(link)


    if vectorstore:
        question = "Extract the final solution to the error"
        answer = retrieve_and_generate(question, vectorstore)
        print(answer)
