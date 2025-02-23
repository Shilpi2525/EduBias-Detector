from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI
import streamlit as st
import os
import PyPDF2
import prompts as pt

#keys
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

#CONSTANTS
MODEL="gpt-4o-mini"

# set the openai model
llm = ChatOpenAI(model=MODEL, temperature=0)

# create client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

#Function 
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    # read the pdf
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # extract the text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()

    final_text = pdf_text.strip().replace("\n", "")        
    return pdf_text



#Function 
def bias_analyser(text: str):
    prompt = ChatPromptTemplate.from_template(pt.BIAS_ANALYSER_PROMPT)
    #model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model=llm
    output_parser = StrOutputParser()

    # create the chain
    chain = prompt | model | output_parser

    # get the answer
    answer = chain.invoke({"text":text})

    return answer
