from operator import itemgetter
import config_data as config
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagService(object):
    def __init__(self):
        self.vecotr_service = VectorStoreService(
            embedding_model=GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-2",
                google_api_key=config.google_api_key
            )
        )

        # MessagesPlaceholder lets us inject prior turns of the conversation
        # so the model can answer follow-up questions with context.
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Provide information concisely based on the provided context: {context}"),
                MessagesPlaceholder("chat_history"),
                ("user", "User question: {input}")
            ]
        )

        self.chat_model = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key=config.google_api_key
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

        # chain now expects a dict input: {"input": str, "chat_history": list[BaseMessage]}
        # "context" is derived by running only the "input" text through the retriever.
        # itemgetter("input") pulls just the question string out of the dict before
        # it reaches the retriever/embedding call (passing the whole dict would break it).
        chain = (
            RunnablePassthrough.assign(
                context=itemgetter("input") | retriever | format_document
            )
            | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        return chain

    @staticmethod
    def _to_lc_messages(chat_history: list[dict]) -> list:
        """Convert simple [{'role': 'user'/'assistant', 'content': str}, ...] into
        LangChain message objects the prompt template can use."""
        lc_messages = []
        for msg in chat_history or []:
            if msg.get("role") == "user":
                lc_messages.append(HumanMessage(content=msg.get("content", "")))
            else:
                lc_messages.append(AIMessage(content=msg.get("content", "")))
        return lc_messages

    def ask(self, question: str, chat_history: list[dict] | None = None) -> str:
        """Ask a question with optional prior conversation history.

        chat_history: list of {"role": "user" | "assistant", "content": str},
        ordered oldest to newest, NOT including the current `question`.
        """
        lc_history = self._to_lc_messages(chat_history)
        return self.chain.invoke({"input": question, "chat_history": lc_history})


if __name__ == "__main__":
    service = RagService()
    history = []

    q1 = "My skin looks warm, which color should I choose?"
    a1 = service.ask(q1, history)
    print(a1)
    history.append({"role": "user", "content": q1})
    history.append({"role": "assistant", "content": a1})

    q2 = "Can you give me an example?"
    a2 = service.ask(q2, history)
    print(a2)