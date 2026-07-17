from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser   

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

input_text = "What is the capital of Germany?"

result = vector_store.similarity_search(input_text,k=1)

reference_text = "#"
for doc in result:
    reference_text += doc.page_content 
reference_text += "#"

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"question":input_text, "context":reference_text})
print(res)
