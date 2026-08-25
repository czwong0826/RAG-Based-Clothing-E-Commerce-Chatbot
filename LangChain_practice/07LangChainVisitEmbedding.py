
from langchain_google_genai import GoogleGenerativeAIEmbeddings


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2", 
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

print(embeddings.embed_query("I like you"))
print(embeddings.embed_documents(["Apple","Orange","Banana"]))