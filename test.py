from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pprint import pprint

folder_path = "./data"  # Replace with the path to your folder

# Get a list of all files in the folder
files = [file for file in os.listdir(
    folder_path) if os.path.isfile(os.path.join(folder_path, file)) and file.endswith('.utf8')]

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    add_start_index=True,
)

# Print the list of files
data = list()
for file in files:
    print(f'Loading {file}')
    loader = BSHTMLLoader(os.path.join(folder_path, file))
    d = loader.load()[0]
    data.append(d)

texts = text_splitter.create_documents(data)
pprint(texts)
