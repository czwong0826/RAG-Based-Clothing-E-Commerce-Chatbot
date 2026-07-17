from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    "What is the capital of {country}? Answer the capital only without any explanation."
)

second_prompts = PromptTemplate.from_template(
    "What is the most famous landmark in {capital}?"
)

my_func = RunnableLambda(lambda ai_msg:{"capital":ai_msg.content})

chain = first_prompt | model | my_func | second_prompts | model | str_parser
res = chain.invoke({"country":"Singapore"})

print(res) 