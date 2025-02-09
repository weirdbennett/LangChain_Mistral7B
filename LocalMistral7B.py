import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

data_loader = TextLoader("data/data.txt", encoding="utf-8")
documents = data_loader.load()

# chunks of data
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

# embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = vector_store.as_retriever()

llm = Ollama(model="mistral")

# query-answering chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

print("Type something.. (to leave pls type 'exit'):")
while True:
    query = input("Question: ")
    if query.lower() == "exit":
        print("Leaving...")
        break
    response = qa_chain.invoke({"query": query})
    print("Answer:", response)