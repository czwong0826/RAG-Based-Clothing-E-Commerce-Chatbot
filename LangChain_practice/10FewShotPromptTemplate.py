from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


example_template = PromptTemplate.from_template('Word:{word}, Antonym:{antonym}')
 
examples_data = [
    {"word":"Big", "antonym":"Small"},
    {"word":"Up", "antonym":"Down"}
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=examples_data,
    prefix="Tell me the antonym of a noun, I will provide the examples:",
    suffix="Based on the previos examples, tell me what is the antonym of {input_word}",
    input_variables=["input_word"]
)

prompt_text = few_shot_template.invoke(input={"input_word":"Left"}).to_string()
print(prompt_text)


from langchain_google_genai import GoogleGenerativeAI
model = GoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)
res = model.invoke(prompt_text)
print(res)