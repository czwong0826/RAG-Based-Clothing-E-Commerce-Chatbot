import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()  # Create the file if it doesn't exist
        return False 
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():  # Ensure the file is readable
            line = line.strip()  # Remove any leading/trailing whitespace
            if line == md5_str:
                return True
    return False


def save_md5(md5_str:str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')  # save the md5 string to the file with a newline character


def get_string_md5(input_string: str, encoding='utf-8'):
    # Create an MD5 hash object
    str_bytes = input_string.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()  # Return the hexadecimal representation of the hash
    
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  # Ensure the directory exists
        # Initialize Chroma instance
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-2",
                google_api_key=config.google_api_key
            ),
            persist_directory=config.persist_directory
        ) 
        # Initialize TextSplitter instance
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #max length of each chunk
            chunk_overlap=config.chunk_overlap, 
            separators=config.separators, 
            length_function=len #python built-in function to calculate the length of a string
        )

    def upload_by_str(self, data:str, filename):
    # convert string to vector and save to ChromaDB
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return (f"File '{filename}' has already been uploaded. Skipping upload.")
        if len(data) > config.max_split_char_length:
            knowledge_chunks : list[str] = self.splitter.split_text(data)  # Split the text into chunks
        else:
            knowledge_chunks = [data]  # If the text is short enough, treat it as a single chunk

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin001"
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]  # Create a list of metadata dictionaries for each chunk
        )

        save_md5(md5_hex)  # Save the MD5 hash to the file after successful upload
        return f"File '{filename}' uploaded successfully with {len(knowledge_chunks)} chunks."

if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("This is a test string for the knowledge base.", "test_file.txt")
    print(r)