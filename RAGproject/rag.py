from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagService(object):
    def __init__(self):
        self.vecotr_service = VectorStoreService(
            embedding_model=GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-2",
                google_api_key="AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
            )
        )

        self.prompt_template =ChatPromptTemplate.from_messages(
            [
                ("system", "Provide information concisely based on the provided context: {context}"),
                ("user", "User question: {input}")
            ]
        )

        self.chat_model = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key="AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
        )

        self.chain = self.__get_chain()


    def __get_chain(self):
        retriever = self.vecotr_service.get_retriever()
    
        def format_document(docs: list[Document]):
            if not docs:
                return "No relevant document found."
            formatted_str = " "
            for doc in docs:
                formatted_str += f"Document: {doc.page_content}\nMetadata: {doc.metadata}\n\n"

            return formatted_str


        chain = (
            {
                "input":RunnablePassthrough(),
                "context": retriever | format_document
            } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        return chain

if __name__ == "__main__":
    res = RagService().chain.invoke("My skin looks warm, which color should I choose?")
    print(res)