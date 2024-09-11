from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_and_store_conversation(conversation_data):

    documents = [Document(page_content=entry['content'], metadata={"author": entry['author']}) for entry in conversation_data]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_texts = splitter.split_documents(documents)

    print("\n=== Split Texts ===")
    for i, text in enumerate(split_texts):
        print(f"Document {i + 1}:")
        print(text.page_content)
        print("\n")

    embeddings = OpenAIEmbeddings(openai_api_key="비밀~")  


    vectorstore = Chroma.from_documents(
        split_texts, embeddings, persist_directory="./chroma_db"
    )


    retrieved_docs = vectorstore.similarity_search("substring", k=5)

    print("\n=== Retrieved Documents from Vector Store ===")
    for i, doc in enumerate(retrieved_docs):
        print(f"Retrieved Document {i + 1}:")
        print(doc.page_content)
        print("\n")

    return vectorstore
