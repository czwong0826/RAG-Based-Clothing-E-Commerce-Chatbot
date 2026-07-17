from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding=GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key="AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )
)

loader = CSVLoader(
    file_path="./LangChain/data/sample.csv",
    encoding="utf-8-sig",  
    source_column="Name"
)

documents = loader.load()
vector_store.add_documents(documents, ids=["id"+str(i) for i in range(1, len(documents)+1)])

vector_store.delete(
     ids=["id5"]
)

print(f"DEBUG: Loaded {len(documents)} documents from CSV.")

result = vector_store.similarity_search(
    query="Who are 20 years old?",
    k=3
)

print(result)


