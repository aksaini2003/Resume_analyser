#here let first make the logic of our resume analyzer agent 
from langgraph.graph import StateGraph,START,END 
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
from typing import TypedDict 
from pydantic import BaseModel 
from langchain.prompts import PromptTemplate
import fitz        # PyMuPDF
# from docx import Document
from pathlib import Path
import streamlit as st 


load_dotenv()

#let add a llm model in our notebook 
groq_key = st.secrets["GROQ_API_KEY"]
llm=ChatGroq(model='Llama-3.3-70b-versatile',api_key=groq_key) 


#now lets make our graph

#state definition
class Graph_Schema(TypedDict):
    resume_text: str 
   
    
    job_description: str 
    review: str 
    
    
graph=StateGraph(Graph_Schema)
    
def Analyzer(state: Graph_Schema)-> Graph_Schema: 
    #now in this node we analyse the resume text and the job_description and make an analysis report on top it 
    prompt=PromptTemplate.from_template(template='''You are a Resume analyser and you have to analyse the given 
    resume and job description 
    first provide  small resume summary and job summary
    You have to create a analysis report after the analysis and you have to return the following things 
    1. What is good and matching 
    2. What is missing in the resume. 
    3. What user can improve in the resume for ATS 
    4. Overall review(also incude rating out of 10)
    
    Job Description - {job_description} 
    
    
    
    
    Resume Text - {resume_text} 
    
    
    
    ''')
    chain= prompt|llm 
    
    #lets invoke our chain 
    resume_text=state['resume_text'] 
    job_description=state['job_description'] 
    response=chain.invoke({'job_description':job_description,'resume_text':resume_text}).content 
    
    state['review']=response
    return state 




#lets make node 
#Here the user will upload the files in the frontend from their we get the resume and job_desc 
graph.add_node('analyzer',Analyzer) 

#edges
 
graph.add_edge(START,'analyzer') 
graph.add_edge('analyzer',END) 

resume_analyzer=graph.compile()