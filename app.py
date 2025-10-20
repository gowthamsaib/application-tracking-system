import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Please add it to your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(
    page_title="Application Tracking System AI",
    layout="wide"
)


# UI Styling 

st.markdown(
    """
<style>
/* Full-page purple gradient background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(1200px circle at 20% 20%, #2b0b55 0%, #1a0635 40%, #110428 70%, #0b031a 100%);
}

/* Hide Streamlit default header space */
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stToolbar"] { right: 2rem; }

/* Make content centered with a max-width */
.main .block-container {
    max-width: 980px;
    padding-top: 70px;
    padding-bottom: 80px;
}

/* Title styling */
.ats-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #ffffff;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.ats-subtitle {
    font-size: 18px;
    color: rgba(255,255,255,0.85);
    margin-bottom: 30px;
}

/* Section label */
.section-label {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255,255,255,0.92);
    margin: 18px 0 10px 0;
}

/* Dark card look for widgets */
div[data-testid="stTextArea"] textarea {
    background: rgba(35, 35, 45, 0.85) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.92) !important;
    border-radius: 14px !important;
    padding: 14px !important;
    min-height: 140px !important;
}

div[data-testid="stFileUploader"] section {
    background: rgba(35, 35, 45, 0.85) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

/* Button styling */
div.stButton > button {
    background: rgba(18, 18, 24, 0.85) !important;
    color: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
}

div.stButton > button:hover {
    border-color: rgba(255,255,255,0.35) !important;
    transform: translateY(-1px);
}

/* Output area styling */
.output-card {
    margin-top: 18px;
    background: rgba(35, 35, 45, 0.65);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 16px 18px;
    color: rgba(255,255,255,0.92);
}

/* Make labels/assist text readable */
label, .stMarkdown, .stText, .stCaption {
    color: rgba(255,255,255,0.92) !important;
}

/* Reduce extra top padding on first element */
[data-testid="stAppViewContainer"] .main .block-container > div:first-child {
    margin-top: 0px;
}
</style>
""",
    unsafe_allow_html=True
)


# Prompt Template

input_prompt = """
You are an experienced Applicant Tracking System (ATS) evaluator with strong knowledge of technical roles,
including software engineering, data science, data analytics, and big data engineering.

Your task is to evaluate the resume against the provided job description and deliver clear, actionable feedback
to improve alignment in a competitive job market.

Calculate an overall match percentage based on the job requirements and identify the most important missing
keywords and skills.

Resume:
{extracted_text}

Job Description:
{jd}

Return the response strictly in the following three sections:
- Job Description Match:
- Missing Keywords:
- Profile Summary:
"""


# UI Layout 

st.markdown('<div class="ats-title">SMART APPLICATION TRACKING SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="ats-subtitle">Improve Your Resume ATS Score</div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">Paste the Job Description</div>', unsafe_allow_html=True)
jd = st.text_area("", placeholder="Paste the job description here...", label_visibility="collapsed")

st.markdown('<div class="section-label">Upload Your Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "",
    type="pdf",
    help="Upload a text-based PDF resume",
    label_visibility="collapsed"
)

submit = st.button("Submit")


# Processing Logic

if submit:
    if uploaded_file is None:
        st.warning("Please upload a resume PDF.")
    elif not jd.strip():
        st.warning("Please paste the job description.")
    else:
        try:
            reader = pdf.PdfReader(uploaded_file)
            extracted_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            if not extracted_text.strip():
                st.error("Unable to extract text from the PDF. Please upload a text-based resume.")
                st.stop()

            final_prompt = input_prompt.format(extracted_text=extracted_text, jd=jd)
            response = model.generate_content(final_prompt)

            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown("ATS Evaluation Result")
            st.write(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")