from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

api_key = "secret"

def retrieve_and_generate(question, vectorstore):


    model = OpenAI(
        openai_api_key=api_key,
        max_tokens=1000,
        temperature=0.0
    )

    template = """
    The following conversation contains multiple error messages and solutions. 
    Identify the final solution that resolved the problem:
    
    Context:
    {context}

    Question:
    {question}
    """
    prompt = PromptTemplate.from_template(template)


    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5},
    )

    context = retriever.get_relevant_documents(question)  

    chain = LLMChain(prompt=prompt, llm=model)

    response = chain.run(context=context, question=question)
    
    return response
