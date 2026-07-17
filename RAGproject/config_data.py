from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

md5_path = str(BASE_DIR / "md5.text")

#Chroma 
collection_name = "rag"
persist_directory = str(BASE_DIR / "chroma_db")

#splitter
chunk_size = 1000 #max length of each chunk
chunk_overlap = 100 #overlap length of each chunk
separators = ["\n\n", "\n", " ", "",".","?","!"] #separators for splitting text
max_split_char_length = 1000 #max length of each chunk after splitting

#
similarity_threshold = 1 # similarity threshold for document retrieval
