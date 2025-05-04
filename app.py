import streamlit as st
import fitz  # PyMuPDF
import spacy
import spacy.cli
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv
import os

# Load API key securely
load_dotenv()
api_key = os.getenv("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")

# App title
st.title("📄 ResumeGPT2: GPT-4 Cover Letter Generator")
st.markdown("Upload your resume and job description to generate a personalized cover letter powered by GPT-4.")

# File uploads
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
job_file = st.file_uploader("📝 Upload Job Description (PDF)", type="pdf")

# Tone selector
tone = st.selectbox("✍️ Choose Cover Letter Tone:", ["Professional", "Confident", "Creative"])

# Optional personalization fields
st.markdown("### ✨ Add Personal Touch (Optional)")
interest = st.text_area("💬 Why are you interested in this job or company?")
goals = st.text_area("🎯 What are your career goals?")
traits = st.text_area("🌟 What qualities, values, or soft skills do you want to highlight?")

# Company Header Fields
st.markdown("### 🏢 Customize Header (Optional)")
company_name = st.text_input("Company Name")
company_address = st.text_area("Company Address")
hiring_manager = st.text_input("Hiring Manager Name")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Extract PDF Text
def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# Extract Keywords
def extract_keywords(text):
    doc = nlp(text)
    return list(set([token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]))

# Template Preview
with st.expander("📋 Preview Template Structure"):
    default_template = (
        "[Today's Date]\n\n"
        "[Hiring Manager Name]\n"
        "[Company Name]\n"
        "[Company Address]\n\n"
        "Dear [Hiring Manager Name],\n\n"
        "I am writing to express my interest in the [Position Title] at [Company Name]. "
        "With my background in [Your Background], I believe I would be a valuable addition to your team.\n\n"
        "Sincerely,\n"
        "[Your Name]"
    )
    st.code(default_template, language="markdown")

# Main Logic
if resume_file and job_file and api_key:
    try:
        resume_text = extract_text(resume_file)
        job_text = extract_text(job_file)

        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_text)
        shared_keywords = set(resume_keywords) & set(job_keywords)

        # Keyword Match Score
        match_score = round(100 * len(shared_keywords) / max(len(job_keywords), 1))
        st.info(f"🧠 Keyword Match Score: {match_score}%")

        if shared_keywords:
            st.sidebar.markdown("### 🔍 Matched Keywords")
            st.sidebar.write(", ".join(sorted(shared_keywords)[:10]))

        # Header for the letter
        today_date = date.today().strftime("%B %d, %Y")
        header = f"""{today_date}

{hiring_manager or '[Hiring Manager Name]'}
{company_name or '[Company Name]'}
{company_address or '[Company Address]'}
"""

        # GPT Prompt
        prompt = f"""
You are a professional resume writer. Write a {tone.lower()} cover letter tailored to the following resume and job description.

Start the letter with the following header exactly (already formatted):

{header}

Then write:
- A strong opening paragraph that shows passion and alignment with the company’s mission.
- One paragraph on education and most relevant experience.
- One paragraph detailing the candidate's technical skills and accomplishments. Include tools or platforms used and quantify results when possible.
- One paragraph incorporating the candidate's stated interest, career goals, and values:
    - Interest: {interest}
    - Goals: {goals}
    - Values: {traits}
- A polished closing that expresses excitement and openness to further discussion.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}

Shared Keywords: {', '.join(shared_keywords)}
"""

        client = OpenAI(api_key=api_key)

        with st.spinner("💬 Generating your cover letter..."):
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
