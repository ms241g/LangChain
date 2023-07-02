import streamlit as st

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = ""

if 'serper_api_key' not in st.session_state:
	st.session_state.serper_api_key = ""

st.set_page_config(page_title="Home", page_icon="🦜️🔗")

st.header("Welcome to LangChain! 👋")

st.markdown(
    """
    [LangChain](https://langchain.readthedocs.io/en/latest) is an open-source framework created to aid the development of applications leveraging the power of large language models (LLMs). It can be used for chatbots, text summarisation, data generation, code understanding, question answering, evaluation, and more 🔥!

    **👈 Provide the API keys in Settings, and select a use case from the sidebar to get started.**

    ##### Web Search
    * A sample app for web search queries using LangChain and Serper API.
    * *Note: The all-in-one search app has been modified to use Serper API instead of SerpApi.*

    ##### URL Summary
    * A sample app for summarizing URL content using LangChain and OpenAI.
    
    ##### Text Summary
    * A sample app for summarizing text using LangChain and OpenAI.
    

    ##### Document Summary
    * A sample app for summarizing documents using LangChain and Chroma.
    

    ##### News Summary
    * A sample app for Google news search and summaries using LangChain and Serper API.
    
    """
)