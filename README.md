# Application Tracking System (ATS)

An AI-powered Application Tracking System built using Streamlit that evaluates how well a resume aligns with a given job description. The system provides an ATS-style match score, identifies missing keywords, and generates a concise professional profile summary to help candidates optimize their resumes for job applications.

---

## Features

- Upload resumes in PDF format  
- Paste and analyze job descriptions  
- Automatic resume text extraction  
- AI-driven ATS evaluation using Google Gemini  
- Outputs:
  - Job Description Match Percentage
  - Missing Keywords
  - Profile Summary  
- Clean and professional Streamlit user interface  

---

## Technology Stack

- Python  
- Streamlit  
- PyPDF2  
- Google Generative AI (Gemini-Pro)  
- python-dotenv  

---


## Project Structure

│
├── app.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore

---

## Usage

- Upload a resume in PDF format
- Paste the corresponding job description
- Click Submit to initiate analysis
- Review the generated ATS insights:
- Resume–Job Description alignment score
- Missing or underrepresented keywords
- Professional profile summary

---

## Notes

- Resume PDFs must contain selectable text; scanned image-based PDFs may not extract correctly
- A valid Google Gemini API key is required for analysis
- This project is intended to simulate ATS-style resume screening logic

---

## Future Enhancements

- Resume optimization and rewrite suggestions
- Support for DOCX resume files
- Multi-job resume comparison
- Skill-level scoring and weighting
- Resume history and tracking dashboard