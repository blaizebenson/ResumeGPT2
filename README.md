# 📄 ResumeGPT2

**ResumeGPT2** is a GPT-4-powered web application that automatically generates tailored cover letters by analyzing a user’s resume and a job description. Built using Streamlit, spaCy, PyMuPDF, and OpenAI’s API, it extracts key skills, aligns them with job requirements, and crafts a professional letter customized by tone, goals, and values.

---

## 🔗 Live Demo

👉 [Launch App on Streamlit](https://resumegpt2-4rikzklkqx3btcpxumsbib.streamlit.app/)

---

## 📂 Features

- 📄 Upload a **Resume (PDF)**
- 📝 Upload a **Job Description (PDF)**
- 🧠 Keyword matching using **spaCy NLP**
- ✍️ Cover letter generation using **OpenAI GPT-4**
- 🗓️ Dynamic insertion of today’s date and company details
- 🎯 Customize letter tone and personalize with your interests, goals, and values
- 📥 Review, edit, and **download the final letter**

---

## 🚀 How to Use

1. Visit the live app using the link above
2. Upload your **resume** and a **job description** (PDF format)
3. Paste your **OpenAI API key** in the secure input field
4. Choose a tone for your letter (e.g., Professional, Confident)
5. Optionally fill in:
   - Your interest in the company
   - Career goals
   - Values or soft skills
   - Company name, address, and hiring manager
6. Click **Generate Cover Letter**
7. Review your personalized GPT-4 cover letter and download it

---

## 💾 Local Development (Optional)

### Requirements
- Python 3.9+
- An OpenAI API key

### Setup

```bash
git clone https://github.com/blaizebenson/ResumeGPT2.git
cd ResumeGPT2
pip install -r requirements.txt
