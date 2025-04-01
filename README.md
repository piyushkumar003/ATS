This Resume Expert System helps candidates optimize their resumes by analyzing them against a Job Description (JD). It leverages Google Gemini (or another generative AI model) to provide insights, percentage matches, improvement suggestions, and identify missing skills and keywords.

Features
PDF Resume Upload: Upload a resume in PDF format.

Job Description Input: Provide a job description to match the resume against.

Gemini AI Model: Uses the Google Gemini AI model to analyze and give insights on the resume based on the job description.

Multiple Evaluation Prompts:

Resume Evaluation: Analyze strengths and weaknesses in the resume.

Resume Improvement: Suggest improvements for the resume to better align with the job description.

Match Percentage: Calculate the percentage match between the resume and job description.

Missing Skills/Keywords: Identify missing skills or keywords in the resume.

Requirements
Python Libraries
To run this system, you will need the following libraries:

streamlit: Web framework to create the interactive app.

google-generative-ai: To interact with Google's generative AI models.

pdf2image: For converting PDFs to images.

Pillow: For image processing.

python-dotenv: To load environment variables such as API keys.

base64: For encoding image data.

io: For handling byte data.

Installation
Clone this repository to your local machine:


git clone https://github.com/yourusername/ats-resume-expert.git
cd ats-resume-expert
Create a virtual environment and activate it:


python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
Install the required libraries:


pip install -r requirements.txt
Or manually install dependencies:


pip install streamlit google-generative-ai pdf2image Pillow python-dotenv
Create a .env file in the root directory and add your Google Gemini API Key:


GOOGLE_API_KEY=your_api_key_here


How to Use
Run the Application:

After setting up the environment, start the Streamlit app with the following command:


streamlit run app.py
Upload Resume: Use the file uploader to upload a resume in PDF format.

Input Job Description: Enter a Job Description (JD) in the text area provided.

Choose Evaluation Type:

Tell me About the Resume: Provides a detailed evaluation of the resume against the JD.

How could I improve my Resume ATS: Suggests improvements to align better with the JD.

Percentage Match with JD: Provides a percentage match between the resume and JD.

What are the Skills/Keywords that are missing: Lists missing skills/keywords.

View Results: After submitting, the results are displayed with a detailed analysis and suggestions.

How It Works
PDF to Image: The uploaded PDF is converted to an image (only the first page) using the pdf2image library.

Base64 Encoding: The image is encoded into base64 format to be passed into the AI model.

Google Gemini AI Model: The system then sends the base64 encoded image along with the job description to the Google Gemini model for processing.

AI Responses: The model provides insights such as strengths, weaknesses, improvement suggestions, missing keywords, and match percentage.

Code Breakdown
1. Gemini Model Integration
The model is initialized with the API key from the .env file and uses the generate_content method to analyze the resume and JD:


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text
2. PDF Handling
The PDF is converted to an image using the pdf2image library and the first page is selected for analysis:


def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    img_byte_arr = img_byte_arr.getvalue()
    
    pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
    return pdf_parts
3. Streamlit Interface
The app is built using Streamlit for an interactive web interface:


st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How could I improve my Resume ATS")
submit3 = st.button("Percentage Match with JD")
submit4 = st.button("What are the Skills/Keywords that are missing")
Future Enhancements
Support for multiple resume pages.

Advanced analysis for resumes in other formats (e.g., DOCX).

More detailed ATS analysis and integration with various ATS tools.

User authentication and storage of analyzed results.

Contributing
Feel free to submit a pull request with bug fixes, improvements, or additional features. Contributions are welcome!

License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
