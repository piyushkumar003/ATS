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
import re



st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# =================== Custom CSS Styling ===================
st.markdown("""
<style>
/* Fancy Buttons */
.stButton > button {
    border-radius: 12px;
    padding: 0.75em 1.5em;
    background-color: #0072E3;
    color: white;
    font-weight: 600;
    font-size: 16px;
    transition: 0.4s;
    box-shadow: 0 4px 14px 0 rgba(0,118,255,0.39);
    border: none;
}
.stButton > button:hover {
    background-color: #005bbb;
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0,118,255,0.45);
    cursor: pointer;
}

/* Background and header */
body {
    background-color: #f4f7fc;
}
h1, h2, h3, h4 {
    color: #2c3e50;
}

h3 {
    color: #2980b9;
}

.highlight {
    color: #e74c3c;
    font-weight: bold;
}

/* Score Box Styling */
.score-box {
    background-color: #2ecc71;
    color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 30px;
}

.sidebar .sidebar-content {
    background-color: #ecf0f1;
    padding: 20px;
}

.stFileUploader {
    border-radius: 12px;
    padding: 10px;
    background-color: #e74c3c;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# =================== Header ===================
# st.markdown("## 📄 ATS Resume Expert")
st.markdown("### ✅ Smart Resume Analyzer ")

# =================== Sidebar ===================
st.sidebar.markdown("### 📌 Instructions")
st.sidebar.markdown("""
1. Upload your **Resume (PDF)**  
2. Paste or type your **Job Description (JD)**  
3. Click any **action button** to evaluate!
""")

st.sidebar.markdown("----")
st.sidebar.info("Built  using Streamlit, Google Gemini Pro, and Python!")

# =================== Helper Functions ===================

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text



def get_enhanced_ats_score(resume_text):
    score = 0
    max_score = 100
    breakdown = {}

    # 1. Section Coverage
    sections = ["experience", "education", "skills", "projects", "summary", "certifications"]
    found_sections = [s for s in sections if s in resume_text.lower()]
    section_score = (len(found_sections) / len(sections)) * 15
    breakdown['Sections'] = round(section_score, 2)

    # 2. Tech Keywords
    tech_keywords = [
        "python", "java", "sql", "machine learning", "data science", "aws", "docker",
        "react", "git", "linux", "pandas", "kubernetes"
    ]
    found_keywords = [kw for kw in tech_keywords if kw in resume_text.lower()]
    keyword_score = (len(found_keywords) / len(tech_keywords)) * 15
    breakdown['Tech Keywords'] = round(keyword_score, 2)

    # 3. Formatting
    format_score = 0
    if "@" in resume_text: format_score += 5
    if re.search(r'\b\d{10}\b', resume_text): format_score += 5
    if "-" in resume_text or "•" in resume_text: format_score += 5
    breakdown['Formatting'] = format_score

    # 4. Grammar & Writing Quality
    # matches = tool.check(resume_text)
    # num_errors = len(matches)
    # grammar_score = max(0, 15 - num_errors)
    # Simple heuristic: count likely grammar issues using bad punctuation patterns (not a full check)
    grammar_penalties = len(re.findall(r"\s{2,}|[^.]\n", resume_text))  # double spaces, missing punctuation
    grammar_score = max(0, 15 - grammar_penalties)
    breakdown['Grammar'] = round(grammar_score, 2)

    # 5. Stats & Numbers
    numbers_found = re.findall(r"\b\d+(\.\d+)?%?\b", resume_text)
    number_score = min(len(numbers_found) * 2, 10)  # cap at 10
    breakdown['Metrics/Numbers'] = round(number_score, 2)

    # 6. Action Verbs
    action_verbs = ["managed", "led", "built", "developed", "created", "increased", "analyzed", "designed"]
    action_verbs_found = [verb for verb in action_verbs if re.search(r'\b' + verb + r'\b', resume_text.lower())]
    verb_score = min(len(action_verbs_found) * 2, 10)
    breakdown['Action Verbs'] = round(verb_score, 2)

    # 7. Soft Skills
    soft_skills = ["communication", "teamwork", "leadership", "adaptability", "problem-solving"]
    soft_found = [s for s in soft_skills if s in resume_text.lower()]
    soft_score = min(len(soft_found) * 2, 10)
    breakdown['Soft Skills'] = round(soft_score, 2)

    # Total Score
    score = sum(breakdown.values())
    return min(score, max_score), breakdown


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
    
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

    

##Streamlit APP

st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input", placeholder="Paste or type the job description here...")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

st.markdown("### 🔍 Choose an Action to Analyze Your Resume:")

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("🧠 Tell me About the Resume")
    submit2 = st.button("🛠 How could I improve my Resume ATS")

with col2:
    submit3 = st.button("📊 Percentage Match with JD")
    submit4 = st.button("🧩 What are the Skills/Keywords that are missing")

# New row just for the submit5 button, centered
center_col1, center_col2, center_col3 = st.columns([1, 2, 1])
with center_col2:
    submit5 = st.button("📈 Check Your ATS Score")




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

input_prompt5 = """
You are an advanced Applicant Tracking System (ATS) evaluator.

Evaluate the uploaded resume based on the following:
- Grammar Quality
- Use of measurable achievements (statistics, numbers, percentages)
- Usage of relevant technical keywords (like 'Python', 'Java', 'SQL', 'Machine-Learning', 'Data Science', 'C', 'C++', etc.)
- Usage of action verbs (like 'Led', 'Developed', 'Managed','Communication', 'Teamwork', 'Leadership', 'Adaptability', 'Problem-Solving', etc.)
- Structure: Does it include key sections like "Experience", "Education", "Skills", "Projects", "Summary", "Certifications"?
- Formatting consistency , Dates in proper order and overall presentation


Give a detailed analysis and a score breakdown on a scale of 100.
Example output:
Grammar: 20/25
Metrics: 15/20
Action Verbs: 10/15
Structure: 20/20
Formatting: 15/20
Overall ATS Score: 80/100

Also give proper weightage to past experience and education.
Make sure to give a score out of 100 and also give the breakdown of the score in the end.
Also just do the scoring like other websites like Resume Worded, Jobscan, Resumake, etc.
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
elif submit4:
    if uploaded_file is not None:
        pdf_parts = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_parts,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")
elif submit5:
    if uploaded_file is not None:
        uploaded_file.seek(0)
        resume_text = extract_text_from_pdf(uploaded_file)
        ats_score, breakdown = get_enhanced_ats_score(resume_text)

        st.markdown(f"<div class='score-box'><h4>📈 ATS Score: <span class='highlight'>{ats_score}/100</span></h4>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Score Breakdown:")
        for key, value in breakdown.items():
            st.markdown(f"- **{key}**: {value}")
    else:
        st.warning("Please upload a PDF file.")
