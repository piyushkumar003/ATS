#field for JD
#upload PDF
#PDF to image-->preprocessing-->Google gemini pro
#prompts template[Multiple Prompts]
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
from io import BytesIO 
import base64
from PIL import Image
# import pdf2image
import fitz
import google.generativeai as genai





genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    # Convert PDF to images
        ## images = pdf2image.convert_from_bytes(uploaded_file.read())

        ## first_page=images[0]
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()

        img = Image.frombytes("RGB", [pix.width,pix.height], pix.samples)

        #convert to bytes
        img_byte_arr = BytesIO()
        # first_page.save(img_byte_arr, format='JPEG')
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64

            }

        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

##Streamlit APP
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell me About the Resume")

submit2= st.button("How could I improve my Resume ATS")

submit3 = st.button("Percentage Match with JD")

submit4 = st.button("What are the Skills/Keywords that are missing")

input_prompt1 = """
You are an experienced HR Manager with Tech skills in the field of any one job role of Software Development,Data Science,Full Stack Development, Big Data Engineering, DEVOPS, Data Aanalyst, Cloud Engineer, 
your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with this.
Highlight the strengths and weaknesses of the applicants in relation to the specified job relation.
"""

input_prompt2 = """
You are an experienced HR Manager with Tech skills in the field of any one job role of Software Development,Data Science,Full Stack Development, Big Data Engineering, DEVOPS, Data Aanalyst, Cloud Engineer, 
your task is to review the provided resume against the job description for these profiles.
Provide me with a detailed analysis of how the candidate can improve their resume to better align with the job description and how should he improve his resume according to Job Description.
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of any one of job role of Software Development,Data Science,Full Stack Development, Big Data Engineering, DEVOPS, Data Aanalyst, Cloud Engineer and deep ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage match against the job description.
First the output should come as percentage.
"""

input_prompt4 = """"
You are an experienced HR Manager with Tech skills in the field of any one job role of Software Development,Data Science,Full Stack Development, Big Data Engineering, DEVOPS, Data Aanalyst, Cloud Engineer, 
your task is to review the provided resume against the job description for these profiles.
Please share the skills/keywords that are missing in the resume against the job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_parts = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_parts,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit2:
    if uploaded_file is not None:
        pdf_parts = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_parts,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit3:
    if uploaded_file is not None:
        pdf_parts = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_parts,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")
else:
    if uploaded_file is not None:
        pdf_parts = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_parts,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")
