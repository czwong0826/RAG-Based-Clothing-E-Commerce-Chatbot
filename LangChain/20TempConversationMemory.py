from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

prompt = PromptTemplate.from_template(
    "You need to answer the question based on the conversastion history. Conversation history:{chat_history}, question: {input}"
)

str_parser = StrOutputParser()
base_chain = prompt | model | str_parser

store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation_chain =RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

if __name__ == "__main__":

    session_config = {
        "configurable":{
            "session_id":"user1"
        }
    }

res = conversation_chain.invoke({"input":"I have one cat"}, session_config)
print("first",res)

res = conversation_chain.invoke({"input":"I have two dogs"}, session_config)
print("second",res)

res = conversation_chain.invoke({"input":"How many pets do I have?"}, session_config)
print("third",res)