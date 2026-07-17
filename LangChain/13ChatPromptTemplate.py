from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are a teacher"),
        MessagesPlaceholder("history"),
        ("human","Can you explain again shortly?")
    ]
)

history_data = [
    ("human","what is the meaning of division?"),
    ("system","Division means...."),
    ("human","what is the meaning of square root?"),
    ("system","Square root is the value that, when multiplied by itself, gives the original number.")
]

prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
print(prompt_text)


from langchain_google_genai import GoogleGenerativeAI
model = GoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key = "AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s"
)

res = model.invoke(prompt_text)
print(res.content)
