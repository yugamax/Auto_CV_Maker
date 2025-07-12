from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = """
You are an expert resume parser and formatter.

Your task is to:
1. Convert the unstructured resume text below into a structured, clean, and consistent JSON format optimized for applicant tracking systems (ATS).
2. Make summary concise and impactful, highlighting key skills and achievements.
3. Do not include any explanations, commentary, or markdown formatting like ```json.
4. Do not include labels like "Output:", "Here's the resume:", etc.
5. If the user includes a custom instruction (e.g., "make it fit on one page" or "convert for fresher"), follow it precisely.
6. If no instruction is given, apply default professional formatting optimized for ATS and readability.
7. Avoid repeating the same action verbs in bullet points — vary language with strong synonyms.
8. Extract and infer important fields even from informal, misaligned, or poorly formatted text.
9. Remove any unnecessary characters, extra whitespace, or line breaks from raw input.
10. Do not use emojis, markdown, informal words, or headings like "Resume Data".
11. If the same category appears more than once under achievements (e.g., "Publication", "Conference Paper"), **combine them into a single entry** with multiple descriptions under the same category instead of repeating.
12. If the resume reflects limited professional experience, intelligently enhance the output by expanding achievements, academic projects, certifications, or summary — to improve balance and professional depth, but only when experience is clearly minimal.
13. In the experience section, when bullet points lack measurable results, enhance them by inferring appropriate outcomes such as performance improvements, time savings, user impact, or scale. Follow the format: [Action] + [What You Did] + [Result/Metric], but only when context supports a logical and realistic enhancement.

---
OUTPUT FORMAT (only return this as plain JSON, no markdown):

{
  "name": "",
  "title": "",
  "phone": "",
  "email": "",
  "linkedin": "",
  "location": "",
  "summary": "",
  "experience": [
    {
      "title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "location": "",
      "points": ["", "", ""]
    }
  ],
  "education": [
    {
      "degree": "",
      "institution": "",
      "start_date": "",
      "end_date": "",
      "location": ""
    }
  ],
  "achievements": [
    {
      "category": "",
      "description": ["", "", ""]
    }
  ],
  "skills": ["", "", "", "..."]
}

---
Resume Text:
\"\"\"{{ resume_text }}\"\"\"

User Instructions (if any):
\"\"\"{{ user_prompt }}\"\"\"
"""


def gen_res(text, user_prompt=""):

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Resume Data:\n{text}\nUser Instruction:\n{user_prompt}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            max_tokens=2048,
        )
        res = completion.choices[0].message.content
        return res
    
    except Exception as e:
        print(f"Error generating resume: {e}")
        return {"error": str(e)}
