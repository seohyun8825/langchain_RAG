from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def process_and_store_conversation(conversation_data):
    """
    store conversation data
    """
    # conversation data to docupent
    documents = [Document(page_content=entry['content'], metadata={"author": entry['author']}) for entry in conversation_data]

    
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    split_texts = splitter.split_documents(documents)

    
    embeddings = OpenAIEmbeddings(openai_api_key="secret")




    vectorstore = Chroma.from_documents(
        split_texts, embeddings, persist_directory="./chroma_db"
    )
    return vectorstore
