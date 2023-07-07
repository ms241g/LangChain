import streamlit as st 

from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.llms import OpenLLM

from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

PATH = 'C:/Users/abc/AppData/Local/nomic.ai/GPT4All/orca-mini-3b.ggmlv3.q4_0.bin'

llm = GPT4All(model=PATH, verbose=True)

prompt = PromptTemplate(input_variables=['question'], template="""
    Question: {question}
    
    Answer: Let's think step by step.
    """)

llm_chain = LLMChain(prompt=prompt, llm=llm)

st.title('🦜🔗 GPT4ALL Y\'All')
st.info('This is using the MPT model!')
prompt = st.text_input('Enter your prompt here!')

if prompt: 
    response = llm_chain.run(prompt)
    print(response)
    st.write(response)