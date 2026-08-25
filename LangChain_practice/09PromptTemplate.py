from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

model = GoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

prompt_template = PromptTemplate.from_template(
    "My lastname is {lastname}, gender is {gender}, what is my lucky number today? short answer"
)

#method 1
#prompt_text = prompt_template.format(lastname="Wong",gender="Male")

#res = model.invoke(prompt_text)
#print(res)

#method2
chain = prompt_template | model
res = chain.invoke({"lastname":"Wong","gender":"Male"})
print(res) 