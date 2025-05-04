import streamlit as st
import fitz  # PyMuPDF
import spacy
import spacy.cli
from openai import OpenAI

# App title
st.title("📄 ResumeGPT2: GPT-4 Cover Letter Generator")
st.markdown("Upload your resume and job description, and get a personalized, professional cover letter powered by GPT-4.")

# File uploads
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
job_file = st.file_uploader("📝 Upload Job Description (PDF)", type="pdf")

# OpenAI API Key input
api_key = st.text_input("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", type="password")

# Ensure spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Helper: Extract PDF text
def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# Helper: Extract relevant keywords
def extract_keywords(text):
    doc = nlp(text)
    return list(set([token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]))

# Main logic
if resume_file and job_file and api_key:
    try:
        resume_text = extract_text(resume_file)
        job_text = extract_text(job_file)

        # Compare and collect shared keywords
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_text)
        shared_keywords = set(resume_keywords) & set(job_keywords)

        # Prepare GPT prompt
        prompt = f"""
You are a professional resume writer. Based on the RESUME and JOB DESCRIPTION below, write a tailored, confident, professional cover letter.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}

Shared Keywords: {', '.join(shared_keywords)}
"""

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        with st.spinner("💬 Generating your custom cover letter using GPT-4..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            cover_letter = response.choices[0].message.content

        st.success("✅ Cover letter generated!")
        st.text_area("📄 Your Cover Letter", cover_letter, height=400)
        st.download_button("📥 Download Letter", data=cover_letter, file_name="cover_letter.txt")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
