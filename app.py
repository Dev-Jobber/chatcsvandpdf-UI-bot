from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time
import functools
import fitz  
import os

load_dotenv()

# API Keys for Google and Groq
google_api_key = os.getenv('google_api_key')
groq_api_key = os.getenv('groq_api_key')

@functools.cache
def llm():
 return ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-70b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    You are a assistant chatbot
    You answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    Don't mention the word 'context' in your response
    If you can not find the answer in the context reply with sorry i don't know
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

@functools.cache
def vector_embedding():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

    pdf_path = "./documents/file.pdf"
    doc = fitz.open(pdf_path)

    docs = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        docs.append(text)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    final_documents = []
    for document in docs:
     chunks = text_splitter.split_text(document)
     final_documents.extend(chunks)

    # Create vector store with embeddings
    vectors = FAISS.from_texts(final_documents, embeddings)
    return vectors

def llm_generator(input_query):
 prompt1 = input_query

 if prompt1:
    vectors = vector_embedding()
    document_chain = create_stuff_documents_chain(llm(), prompt)
    retriever = vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({'input': prompt1})
    
    
    # print document similarity results
    print("\nDocument Similarity Search:")
    for i, doc in enumerate(response["context"]):
        print(doc.page_content)
        print("--------------------------------")
        
        
    print("Response time:", time.process_time() - start)
    print("Answer:", response['answer'])
    return response['answer']

