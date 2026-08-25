from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

model = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

prompt = PromptTemplate.from_template(
"My neighbor surname {surname}, his child's gender is {gender}, give his child a name, no need to give other information"
)

parser = StrOutputParser()

chain = prompt | model | parser | model
res = chain.invoke({
    "surname":"Wong",
    "gender":"Male"
    })

print(res)

