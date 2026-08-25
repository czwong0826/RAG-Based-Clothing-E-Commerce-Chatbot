from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path=r"LangChain\data\sample.csv",  # Use raw string to avoid escape sequence warnings
    encoding="utf-8"
)

#documents = loader.load()

for document in loader.lazy_load():
    print(document)