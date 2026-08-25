from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model = ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )

messages = [
    SystemMessage(content="You are a teacher"),
    HumanMessage(content="what is the meaning of division?"),
    AIMessage(content="Division means....For example,..."),
    HumanMessage(content="what is the meaning of square root?")
]

res = model.stream(input=messages)
for chunk in res:
    print(chunk.content, end="",flush=True)