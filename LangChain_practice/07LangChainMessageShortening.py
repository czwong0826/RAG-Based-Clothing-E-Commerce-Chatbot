from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model = ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )

messages = [
    ("system","you are a teacher"),
    ("human","what is the meaning of Aggresive?"),
    ("ai","Aggresive means..."),
    ("human","what is the meaning of abbreviation?")
    ]

res = model.stream(input=messages)
for chunk in res:
    print(chunk.content, end="",flush=True)