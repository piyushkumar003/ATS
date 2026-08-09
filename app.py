import os
import io
import re
import base64
from io import BytesIO
from datetime import datetime
from PIL import Image
import pymupdf as fitz
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# =================== Page Configuration ===================
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    width: 100%;
}
.stButton > button:hover {
    background-color: #005bbb;
    transform: scale(1.02);
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
st.markdown("### ✅ Smart Resume Analyzer")

# =================== Sidebar ===================
st.sidebar.markdown("### 📌 Instructions")
st.sidebar.markdown("""
1. Upload your **Resume (PDF)**  
2. Paste or type your **Job Description (JD)**  
3. Click any **action button** to evaluate!
""")

st.sidebar.markdown("----")
st.sidebar.info("Built using Streamlit, Groq AI, and Python!")

# =================== Helper Functions ===================

def get_gemini_response(input_text, pdf_content, prompt):
    current_date = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year

    messages = [
        {
            "role": "system",
            "content": (
                f"CRITICAL SYSTEM INSTRUCTION:\n"
                f"Today's exact date is {current_date} (Year {current_year}).\n"
                f"Any resume dates up to {current_year} (including 2025 and 2026) are CURRENT OR PAST DATES.\n"
                f"DO NOT assume the year is 2024. DO NOT flag 2025 or 2026 dates as future, placeholders, or typos.\n"
                f"Keep internal reasoning concise and ensure a complete, detailed final evaluation is delivered."
            )
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": input_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{pdf_content[0]}"
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    response = client.chat.completions.create(
        model='qwen/qwen3.6-27b',
        messages=messages,
        max_tokens=4096,
        temperature=0.6
    )
    
    raw_content = response.choices[0].message.content or ""
    
    # Cleanly strip <think>...</think> reasoning blocks
    if "<think>" in raw_content:
        if "</think>" in raw_content:
            result = raw_content.split("</think>")[-1].strip()
        else:
            result = re.sub(r'<think>.*', '', raw_content, flags=re.DOTALL).strip()
    else:
        result = raw_content.strip()

    if not result:
        result = "Unable to generate evaluation. Please try submitting again."

    return result

def get_enhanced_ats_score(resume_text):
    max_score = 100
    breakdown = {}

    # 1. Section Coverage (Max: 20)
    sections = ["experience", "education", "skills", "projects", "summary", "certifications"]
    found_sections = [s for s in sections if s in resume_text.lower()]
    section_score = min((len(found_sections) / 4) * 20, 20)
    breakdown['Sections'] = round(section_score, 2)

    # 2. Tech Keywords (Max: 20)
    tech_keywords = [
        "python", "java", "sql", "machine learning", "data science", "aws", "docker",
        "react", "git", "linux", "pandas", "kubernetes", "c++", "c", "javascript", "html", "css", "api"
    ]
    found_keywords = [kw for kw in tech_keywords if kw in resume_text.lower()]
    keyword_score = min((len(found_keywords) / 5) * 20, 20)
    breakdown['Tech Keywords'] = round(keyword_score, 2)

    # 3. Formatting (Max: 15)
    format_score = 5
    if "@" in resume_text: 
        format_score += 5
    if re.search(r'\b\d{10}\b', resume_text): 
        format_score += 5
    breakdown['Formatting'] = format_score

    # 4. Grammar & Writing Quality (Max: 15)
    grammar_score = 15 
    breakdown['Grammar'] = round(grammar_score, 2)

    # 5. Stats & Numbers (Max: 10)
    numbers_found = re.findall(r"\b\d+(\.\d+)?%?\b", resume_text)
    number_score = min(len(numbers_found) * 2, 10)
    breakdown['Metrics/Numbers'] = round(number_score, 2)

    # 6. Action Verbs (Max: 10)
    action_verbs = ["managed", "led", "built", "developed", "created", "increased", "analyzed", "designed", "implemented", "resolved"]
    action_verbs_found = [verb for verb in action_verbs if re.search(r'\b' + verb + r'\b', resume_text.lower())]
    verb_score = min(len(action_verbs_found) * 2, 10)
    breakdown['Action Verbs'] = round(verb_score, 2)

    # 7. Soft Skills (Max: 10)
    soft_skills = ["communication", "teamwork", "leadership", "adaptability", "problem-solving", "collaboration", "agile"]
    soft_found = [s for s in soft_skills if s in resume_text.lower()]
    soft_score = min(len(soft_found) * 2, 10)
    breakdown['Soft Skills'] = round(soft_score, 2)

    score = sum(breakdown.values())
    return min(score, max_score), breakdown

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        uploaded_file.seek(0)
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        img_bytes = img_byte_arr.getvalue()

        pdf_parts = [
            base64.b64encode(img_bytes).decode('utf-8')
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# =================== Streamlit APP ===================

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

center_col1, center_col2, center_col3 = st.columns([1, 2, 1])
with center_col2:
    submit5 = st.button("📈 Check Your ATS Score")

# =================== Prompts Definition ===================

input_prompt1 = """
You are an experienced HR Manager with Tech skills in Software Development, Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analysis, or Cloud Engineering.
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with this.
Highlight the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt2 = """
You are an experienced HR Manager with Tech skills in Software Development, Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analysis, or Cloud Engineering.
Your task is to review the provided resume against the job description for these profiles.
Provide me with a detailed analysis of how the candidate can improve their resume to better align with the job description.
Additionally, evaluate the resume's formatting: check if experience and education are listed in reverse chronological order, and verify that date formats are strictly consistent throughout the document. Highlight any inconsistencies.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Software Development, Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analysis, and Cloud Engineering roles.
Your task is to evaluate the resume against the provided job description. Give me the percentage match against the job description.
First, display the percentage match clearly at the top of your response.
"""

input_prompt4 = """
You are an experienced HR Manager with Tech skills in Software Development, Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analysis, or Cloud Engineering.
Your task is to review the provided resume against the job description for these profiles.
Please share the specific technical and soft skills/keywords that are missing from the resume relative to the job description.
"""

input_prompt5 = """
You are an advanced Applicant Tracking System (ATS) evaluator.

Evaluate the uploaded resume based on the following:
- Grammar Quality
- Use of measurable achievements (statistics, numbers, percentages)
- Usage of relevant technical keywords (like 'Python', 'Java', 'SQL', 'Machine-Learning', 'Data Science', 'C', 'C++', etc.)
- Usage of action verbs (like 'Led', 'Developed', 'Managed','Communication', 'Teamwork', 'Leadership', 'Adaptability', 'Problem-Solving', etc.)
- Structure: Does it include key sections like "Experience", "Education", "Skills", "Projects", "Summary", "Certifications"?
- Formatting consistency, dates in proper order, and overall presentation.

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
Do the scoring similar to Resume Worded, Jobscan, and Resumake.
"""

# =================== Execution Handlers ===================

if submit1:
    if uploaded_file is not None:
        with st.spinner("Analyzing resume content..."):
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit2:
    if uploaded_file is not None:
        with st.spinner("Generating improvement recommendations..."):
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt2)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit3:
    if uploaded_file is not None:
        with st.spinner("Calculating percentage match..."):
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit4:
    if uploaded_file is not None:
        with st.spinner("Extracting missing skills and keywords..."):
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt4)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload a PDF file")

elif submit5:
    if uploaded_file is not None:
        with st.spinner("Computing ATS score..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            ats_score, breakdown = get_enhanced_ats_score(resume_text)

            st.markdown(f"<div class='score-box'><h4>📈 ATS Score: <span class='highlight'>{ats_score}/100</span></h4></div>", unsafe_allow_html=True)
            st.markdown("#### 🔍 Score Breakdown:")
            for key, value in breakdown.items():
                st.markdown(f"- **{key}**: {value}")
    else:
        st.warning("Please upload a PDF file.")
