import streamlit as st
import pypdf
import os, tempfile
import openai
import pinecone
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


import os
os.environ['OPENAI_API_KEY'] = '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'

# Set API keys from session state
#openai_api_key = st.session_state.openai_api_key
OPENAI_API_KEY = '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'

st.set_page_config(page_title="Home", page_icon="🦜️🔗")                                                                                            
st.header("Welcome to Document Search! 👋")

# Streamlit app
st.subheader('Document search using query')
source_doc = st.file_uploader('Upload your files', accept_multiple_files=True, type=['pdf'])

search_query = st.text_input("Enter Search Query")


def split_docs(documents, chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs


def get_similiar_docs(query, k=3, score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query, k=k)
  else:
    similar_docs = index.similarity_search(query, k=k)
    print('Similar docs: ', similar_docs)
  return similar_docs


def get_answer(query):
  similar_docs = get_similiar_docs(query)
  answer = chain.run(input_documents=similar_docs, question=query)
  return answer



# If the 'Summarize' button is clicked
if st.button("Search Document"):
    # Validate inputs
    if not OPENAI_API_KEY:
        st.error("Please provide the missing API keys in Settings.")
    elif not source_doc:
        st.error("Please provide the source document.")
    else:
        try:
            with st.spinner('Please wait...'):
              print('In spinner with loop')
              # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
              with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                  print('in tempfile loop')
                  for f in source_doc:
                    tmp_file.write(f.read())
                    
              print('before loader')
              loader = PyPDFLoader(tmp_file.name)
              pages = loader.load_and_split()
              os.remove(tmp_file.name)
              
              docs = split_docs(pages)

            # Create embeddings for the pages and insert into Chroma database
              print('before embeddings')
              embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
              pinecone.init(api_key="5fa93803-7e20-44c1-8ac5-7c2b18a6cd2c", environment="us-west1-gcp-free")
              index_name = "langchain-index"
              index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
            #vectordb = Chroma.from_documents(pages, embeddings)

              # Initialize the OpenAI module, load and run the summarize chain
              model_name = "text-davinci-003"
              llm = OpenAI(model_name=model_name)
              #llm=OpenAI(temperature=0, openai_api_key=openai_api_key)
              chain = load_qa_chain(llm, chain_type="stuff")

              #search = vectordb.similarity_search(" ")
              #summary = chain.run(input_documents=search, question="Write a summary within 200 words.")
              answer = get_answer(search_query)
              st.success(answer)
        except Exception as e:
            st.exception(f"An error occurred: {e}")