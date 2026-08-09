📄 Smart Resume Analyzer (ATS Resume Expert)
An AI-powered Applicant Tracking System (ATS) Resume Expert built with Streamlit, Groq AI (qwen/qwen3.6-27b), and PyMuPDF (fitz). This tool helps job seekers optimize their resumes against specific Job Descriptions (JDs) by providing qualitative AI insights, match percentages, skill gap analysis, and a local heuristic ATS score.

🚀 Features
📑 PDF Resume Upload: Directly upload resumes in PDF format.

📝 Job Description Matching: Compare your resume against any job description.

⚡ Groq AI Integration: Powered by qwen/qwen3.6-27b on Groq's high-speed inference engine.

🔍 5 Evaluation Actions:

Tell me About the Resume: Professional HR evaluation highlighting strengths and weaknesses.

How could I improve my Resume ATS: Actionable feedback, chronological ordering check, and date consistency checks.

Percentage Match with JD: Quantified match score based on qualifications and alignment.

Missing Skills/Keywords: Clear list of critical hard and soft skills absent from the resume.

Check Your ATS Score: Instant local 100-point heuristic breakdown (Sections, Tech Keywords, Action Verbs, Metrics, Formatting, Soft Skills, and Grammar).

🛠 Tech Stack & Requirements
Frontend & App Framework: Streamlit

LLM Engine: Groq API (qwen/qwen3.6-27b)

PDF & Image Processing: PyMuPDF (fitz), Pillow (PIL)

Environment Management: python-dotenv

📦 Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/yourusername/ats-resume-expert.git
cd ats-resume-expert
2. Set Up a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Create a requirements.txt file (or install directly):

Bash
pip install streamlit groq pymupdf Pillow python-dotenv
4. Environment Variables Configuration
Create a .env file in the root directory and add your Groq API Key:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
🔑 Get your API Key from the Groq Console.

💻 Running the Application
Launch the Streamlit web application:

Bash
streamlit run app.py
Upload Resume: Drag and drop or browse your PDF resume.

Enter JD: Paste the job description into the text area.

Analyze: Click any of the 5 action buttons to generate analysis and scores.

🧠 Code Architecture & How It Works
1. Groq LLM Integration & System Prompt Safeguards
Sends vision payloads (converted page image) and text inputs to qwen/qwen3.6-27b via Groq. Features dynamic real-time date anchors to avoid false "future date" warnings and includes automated regex cleaning to strip internal <think> reasoning tags:

Python
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model='qwen/qwen3.6-27b',
    messages=messages,
    max_tokens=4096,
    temperature=0.6
)
# Cleanly strips internal thought tags from reasoning models
result = re.sub(r'<think>.*?(?:</think>|$)', '', raw_content, flags=re.DOTALL).strip()
2. PDF to Base64 Image Conversion (PyMuPDF)
Replaces pdf2image and Poppler binary dependencies with pure PyMuPDF (fitz), rendering first-page previews into base64 JPEG strings for LLM vision analysis:

Python
import pymupdf as fitz

pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
first_page = pdf_document.load_page(0)
pix = first_page.get_pixmap()

img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
3. Local Heuristic ATS Scoring Engine
Calculates a 100-point breakdown across key resume metrics instantly without API latency:

Python
def get_enhanced_ats_score(resume_text):
    # Evaluates Sections, Technical Keywords, Action Verbs,
    # Metrics/Numbers, Soft Skills, Formatting, and Grammar.
    ...
🔮 Future Enhancements
📄 Multi-page PDF visual analysis support.

📑 Support for Word Documents (.docx).

📥 Export analysis reports as downloadable PDFs.

🎯 Role-specific prompt customizers (e.g., SDE, Data Engineering, Product Management).

📜 License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
