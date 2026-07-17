from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path = "./LangChain/data/stu_json_lines.json",
    jq_schema = ".name",
    text_content=False, # True = convert JSON to text, False = keep as structured data
    json_lines=True # Each line is a separate JSON object, only use in JSON Lines format
)

document = loader.load()
print(document)