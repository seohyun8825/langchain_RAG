from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
def process_and_store_conversation(conversation_data):
    documents = []
    for entry in conversation_data:
        content = entry.get('content', '').strip()
        # user -> problem을 얘기하고, gpt는 solution을 내놓음
        doc_type = 'problem' if entry['author'] == 'user' else 'solution'
        print(f"Storing {doc_type} Document: {content[:500]}") 

        if content:
            documents.append(Document(page_content=content, metadata={"author": entry['author'], "type": doc_type}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_texts = splitter.split_documents(documents)


    for i, text in enumerate(split_texts):
        print(f"Stored Document {i + 1} Metadata: {text.metadata}")
        print(f"Stored Document {i + 1} Content (First 500 chars): {text.page_content[:500]}")

    embeddings = OpenAIEmbeddings(openai_api_key="secret")
    vectorstore = Chroma.from_documents(split_texts, embeddings, persist_directory="./chroma_db")

    return vectorstore


def search_by_type(vectorstore, doc_type="problem", query="error"):

    results = vectorstore.similarity_search(query, k=10)

    filtered_results = [doc for doc in results if doc.metadata.get("type") == doc_type]

    print(f"\n=== Retrieved {doc_type.capitalize()} Documents ===")
    if not filtered_results:
        print(f"WARNING: No {doc_type} documents found.")
    else:
        for i, doc in enumerate(filtered_results):
            print(f"Retrieved Document {i + 1} Metadata: {doc.metadata}")
            print(f"Retrieved Document {i + 1} Content (First 500 chars):\n{doc.page_content[:500]}\n")

    return filtered_results
