from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

api_key = "비밀~"

def retrieve_and_generate(question, vectorstore):

    model = OpenAI(
        openai_api_key=api_key,
        max_tokens=1000,
        temperature=0.0
    )

    template = """
    The following is a step-by-step explanation of how to resolve the code issue encountered:

    1. **Initial Code**:
    The user's original code was:
    ```python
    {context_code}
    ```

    2. **Identified Problem**:
    The error that occurred in the code was:
    **Error**: {error_description}

    This happened because:
    **Cause**: {cause_description}

    3. **Solution Steps**:
    Based on the conversation, here are the steps to resolve the issue:
    Step 1: {step_1}
    Step 2: {step_2}

    4. **Final Working Code**:
    After applying the fixes, the final solution code is:
    ```python
    {final_solution_code}
    ```

    Question:
    {question}
    """
    prompt = PromptTemplate.from_template(template)


    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5},
    )

    context_documents = retriever.get_relevant_documents(question)

    if not context_documents:
        print("No relevant documents found.")
        return "No relevant documents found."

    for i, doc in enumerate(context_documents):
        print(f"Retrieved Document {i+1} Content:\n{doc.page_content[:500]}\n")

    code_patterns = ["```python", "```js", "function", "async", "await", "const", "let", "var", "#", "//", "/*", "*/"]


    context_code = next(
        (doc.page_content for doc in context_documents if any(pattern in doc.page_content for pattern in code_patterns)),
        "No initial code found."
    )

    error_description = next((doc.page_content for doc in context_documents if "Error:" in doc.page_content), "No error description found.")
    cause_description = next((doc.page_content for doc in context_documents if "Cause:" in doc.page_content), "No cause description found.")
    step_1 = next((doc.page_content for doc in context_documents if "Step 1:" in doc.page_content), "Step 1 solution not found.")
    step_2 = next((doc.page_content for doc in context_documents if "Step 2:" in doc.page_content), "Step 2 solution not found.")
    final_solution_code = next((doc.page_content for doc in context_documents if "Final Solution" in doc.page_content), "No final solution code found.")


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