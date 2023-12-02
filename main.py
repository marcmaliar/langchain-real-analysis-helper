from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pprint import pprint
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langserve import add_routes
from fastapi import FastAPI

folder_path = "./data"  # Replace with the path to your folder

# Get a list of all files in the folder
files = [file for file in os.listdir(
    folder_path) if os.path.isfile(os.path.join(folder_path, file)) and file.endswith('.utf8')]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # now I'm playing around with these numbers
    length_function=len,
    add_start_index=True,
)

# Print the list of files
documents = list()
for file in files:
    print(f'Loading {file}')
    loader = BSHTMLLoader(os.path.join(folder_path, file))
    document = loader.load()[0]
    documents.append(document)

split_documents = text_splitter.split_documents(
    documents)  # not create_documents
# create documents is from text not documents already (which have metadata, we like metadata)
pprint(split_documents)

embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(split_documents, embeddings)
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = ChatOpenAI(model_name="gpt-4")
memory = ConversationSummaryMemory(
    llm=llm, memory_key="chat_history", return_messages=True
)
qa = ConversationalRetrievalChain.from_llm(
    llm, retriever=retriever, memory=memory)

# 2. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# 3. Adding qa route
add_routes(
    app,
    qa,
    path="/test",
)
