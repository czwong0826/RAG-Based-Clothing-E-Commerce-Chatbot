from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI


model = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

first_prompt = PromptTemplate.from_template(
    "What is the capital of {country}? Answer in JSON format with the key 'capital' and value as the answer"
)

second_prompts = PromptTemplate.from_template(
    "How famous is the {capital}?"
)

chain = first_prompt | model | json_parser | second_prompts | model | str_parser
res = chain.stream({"country":"Malaysia"})
for chunk in res:
    print(chunk, end="", flush=True)