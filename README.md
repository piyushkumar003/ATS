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
