import streamlit as st 
import fitz 
from pathlib import Path
from PyPDF2 import PdfReader
from backend import resume_analyzer 
# def extract_text(uploaded_file):
#     reader = PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# NOTE: Here We are checking the different variety of libraries for the text extraction and pickup the best one

import io

def extract_text(uploaded_file):
    # Read the uploaded file into memory
    file_bytes = uploaded_file.read()
    pdf_stream = io.BytesIO(file_bytes)

    # Open the PDF using PyMuPDF
    doc = fitz.open(stream=pdf_stream, filetype="pdf")

    # Extract text from each page
    text = ""
    for page in doc:
        text += page.get_text()
    return text

    


#for providing user a interface for uploading the pdf files like 
st.header('Upload Your Resume Here: ')
uploaded_resume = st.file_uploader('Upload a file',key='resume') #for making multiple components we have to give key to them 
resume: str
if uploaded_resume:
    resume=extract_text(uploaded_resume) 
    

st.header('Upload The Job Description Here: ')
uploaded_job_description = st.file_uploader('Upload a file',key='job_desc')
#now we can handle them like a pdf using fitz 
job_desc: str
if uploaded_job_description:
    job_desc=extract_text(uploaded_job_description)
    

#after getting the both job desc and the resume we can invoke our workflow through it 
if uploaded_job_description and uploaded_resume:
    analyze=st.button('Analyze')
    if analyze:
        output_state= resume_analyzer.invoke({'resume_text':resume,'job_description':job_desc})
        st.write(output_state['review'])
#and now we have to print the generated analysis resume and job through our system 

