from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser   
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","Based on the following documents, concise answer the question. Reference documents:{context}"),
        ("human","User ask: {question}")  
    ]
)

vector_store = InMemoryVectorStore(
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key="AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )
)

vector_store.add_texts(
    ["The capital of France is Paris.", "The capital of Germany is Berlin.","The capital of Italy is Rome."],     
)


retriever = vector_store.as_retriever(search_kwargs={"k":1}) #return a runnable interface so that we can use it in the chain

def format_func(docs: list[Document]):
    if not docs:
        return "No relevant document found."
    
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content + ", "
    formatted_str += "]"

    return formatted_str


def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt


chain = ({"question":RunnablePassthrough(), "context": retriever | format_func}) | prompt | print_prompt | model | StrOutputParser()

input_text = "What is the capital of Germany?"

res = chain.invoke( input_text)
print(res)
