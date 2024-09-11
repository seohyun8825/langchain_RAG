from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
from vector_store import search_by_type 
api_key = "secret"
import logging

def retrieve_and_generate(question, vectorstore, doc_type="problem"):
    try:
        logging.debug(f"Querying for {doc_type} with question: {question}")


        results = search_by_type(vectorstore, doc_type=doc_type, query=question)
        
        if not results:
            logging.warning(f"No {doc_type} documents found.")
            return f"No {doc_type} documents found."

        logging.debug(f"Found {len(results)} {doc_type} documents.")

        context_code = extract_code_from_docs(results)
        error_description = extract_error_description(results)
        cause_description = extract_cause_description(results)
        step_1 = extract_step(results, "Step 1")
        step_2 = extract_step(results, "Step 2")
        final_solution_code = extract_final_solution_code(results)

        model = OpenAI(openai_api_key=api_key, max_tokens=1000, temperature=0.0)

        template = """
        The following is a step-by-step explanation of how to resolve the code issue encountered:

        1. **Initial Code**:
        ```python
        {context_code}
        ```

        2. **Identified Problem**:
        **Error**: {error_description}
        **Cause**: {cause_description}

        3. **Solution Steps**:
        Step 1: {step_1}
        Step 2: {step_2}

        4. **Final Working Code**:
        ```python
        {final_solution_code}
        ```

        Question:
        {question}
        """

        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(prompt=prompt, llm=model)

        response = chain.run(
            context_code=context_code,
            error_description=error_description,
            cause_description=cause_description,
            step_1=step_1,
            step_2=step_2,
            final_solution_code=final_solution_code,
            question=question
        )

        return response
    except Exception as e:
        logging.error(f"Error during retrieval and generation: {e}")
        return str(e)

def extract_code_from_docs(docs):
    for doc in docs:
        if "```python" in doc.page_content:
            return doc.page_content
    return "No code found."

def extract_error_description(docs):
    for doc in docs:
        if "Error:" in doc.page_content:
            return doc.page_content
    return "No error description found."

def extract_cause_description(docs):
    for doc in docs:
        if "Cause:" in doc.page_content:
            return doc.page_content
    return "No cause description found."

def extract_step(docs, step):
    for doc in docs:
        if step in doc.page_content:
            return doc.page_content
    return f"{step} solution not found."

def extract_final_solution_code(docs):
    for doc in docs:
        if "Final Solution" in doc.page_content:
            return doc.page_content
    return "No final solution code found."