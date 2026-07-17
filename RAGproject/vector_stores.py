from langchain_chroma import Chroma
import config_data as config



class VectorStoreService(object):

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = Chroma(
            collection_name = config.collection_name,
            embedding_function = self.embedding_model,
            persist_directory = config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == "__main__":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    retriever = VectorStoreService(GoogleGenerativeAIEmbeddings(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )).get_retriever()

    res = retriever.invoke("My skin looks warm, which color should I choose? Briefly answer.")
    print(res)