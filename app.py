import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# Application Tracking System AI
# Author: Gowtham


# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found. Please add it to your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")


# Streamlit Page Configuration

st.set_page_config(
    page_title="Application Tracking System AI",
    layout="centered"
)


# Minimal Styling (No Background Image)

page_style = """
<style>
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)


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


# Streamlit UI

st.title("APPLICATION TRACKING SYSTEM AI")
st.text("AI-based Resume Evaluation for Job Description Alignment")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type="pdf",
    help="Upload a text-based PDF resume"
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
                    extracted_text += text

            if not extracted_text.strip():
                st.error("Unable to extract text from the PDF. Please upload a text-based resume.")
                st.stop()

            final_prompt = input_prompt.format(
                extracted_text=extracted_text,
                jd=jd
            )

            response = model.generate_content(final_prompt)

            st.subheader("ATS Evaluation Result of the Resume")
            st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")