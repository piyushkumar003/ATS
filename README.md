# 📄 Smart Resume Analyzer (ATS Resume Expert)

An AI-powered Applicant Tracking System (ATS) Resume Expert built with **Streamlit**, **Groq AI (`qwen/qwen3.6-27b`)**, and **PyMuPDF (`fitz`)**. This tool helps job seekers optimize their resumes against specific Job Descriptions (JDs) by providing qualitative AI insights, match percentages, skill gap analysis, and a local heuristic ATS score.

---

## 🚀 Features

- 📑 **PDF Resume Upload**: Directly upload resumes in PDF format.
- 📝 **Job Description Matching**: Compare your resume against any job description.
- ⚡ **Groq AI Integration**: Powered by `qwen/qwen3.6-27b` on Groq's high-speed inference engine.
- 🔍 **5 Evaluation Actions**:
  1. **Tell me About the Resume**: Professional HR evaluation highlighting strengths and weaknesses.
  2. **How could I improve my Resume ATS**: Actionable feedback, chronological ordering check, and date consistency checks.
  3. **Percentage Match with JD**: Quantified match score based on qualifications and alignment.
  4. **Missing Skills/Keywords**: Clear list of critical hard and soft skills absent from the resume.
  5. **Check Your ATS Score**: Instant local 100-point heuristic breakdown (Sections, Tech Keywords, Action Verbs, Metrics, Formatting, Soft Skills, and Grammar).

---

## 🛠 Tech Stack & Requirements

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Groq API](https://console.groq.com/) (`qwen/qwen3.6-27b`)
- **PDF & Image Processing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/), [Pillow (PIL)](https://python-pillow.org/)
- **Environment Management**: [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/ats-resume-expert.git](https://github.com/yourusername/ats-resume-expert.git)
cd ats-resume-expert
```



### 2. Set Up a Virtual Environment
Windows
```
python -m venv venv
venv\Scripts\activate
```

macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages directly:
```
pip install streamlit groq pymupdf Pillow python-dotenv
```

4. Environment Variables Configuration
Create a .env file in the root directory and add your Groq API Key:
```
GROQ_API_KEY=your_groq_api_key_here
```

💻 Running the Application
Launch the Streamlit web application:
```
streamlit run app.py
```
Upload Resume: Drag and drop or browse your PDF resume.

Enter JD: Paste the job description into the text area.

Analyze: Click any of the 5 action buttons to generate analysis and scores.

# 🔮 Future Enhancements

📄 Multi-page PDF visual analysis support.

📑 Support for Word Documents (.docx).

📥 Export analysis reports as downloadable PDFs.

🎯 Role-specific prompt customizers (e.g., SDE, Data Engineering, Product Management).

📜 License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
