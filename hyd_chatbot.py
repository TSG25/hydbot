# -*- coding: utf-8 -*-
"""hyd-chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16WxhOh2mrpzlMrlsqiBvI54CyAXxwghv
"""

!git clone https://github.com/TSG25/hyddata.git

!pip install gpt-index
!pip install langchain

!pip install llama-index

from llama_index import SimpleDirectoryReader, GPTListIndex , StorageContext, load_index_from_storage,readers, GPTVectorStoreIndex,LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown,display

def construct_index (hyddata):
    max_input_size = 4096
    num_outputs = 300
    max_chunk_overlap =20
    chunk_size_limit = 600

    llm_predictor =LLMPredictor(llm=OpenAI(temperature=0.5,model_name= "davinci-002", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size,num_outputs, 0.5,chunk_size_limit=chunk_size_limit)
    documents = SimpleDirectoryReader(hyddata).load_data()

    index = GPTVectorStoreIndex(
                   documents, llm_predictor=llm_predictor,prompt_helper=prompt_helper )
    index.storage_context.persist(persist_dir="index.json")
    return index

def ask_ai():
  storage_context =StorageContext.from_defaults(persist_dir="index.json")
  index= load_index_from_storage(storage_context)
  query_engine = index.as_query_engine()
  while True:
    query = input("what do you want to ask?")
    response = query_engine.query(query)
    display(Markdown(f"Response: <b>{response.response}</b>"))

os.environ["OPENAI_API_KEY"]= input("Paste your api key here:")

construct_index("hyddata")

ask_ai()