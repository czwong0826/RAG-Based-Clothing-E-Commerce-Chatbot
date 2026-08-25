# from langchain_community.llms.openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash-lite",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
    )

res = model.invoke(input ="who are you in one short sentence")
print(res)