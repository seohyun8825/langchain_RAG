from conversation_extractor import fetch_conversation_from_link
from vector_store import process_and_store_conversation
from rag_retrieve import retrieve_and_generate

def export_and_store_conversation(conversation_link):
    conversation_data = fetch_conversation_from_link(conversation_link)
    if conversation_data:
        vectorstore = process_and_store_conversation(conversation_data)
        return vectorstore
    else:
        print("Failed to fetch or store the conversation.")
        return None

if __name__ == "__main__":
    link = "https://chatgpt.com/share/68e6ee7c-23ee-4527-bf3d-7d4d4f4e98f8"

    vectorstore = export_and_store_conversation(link)

    if vectorstore:
        question = "Extract the final solution to the error"
        answer = retrieve_and_generate(question, vectorstore, doc_type="problem")
        print(answer)
