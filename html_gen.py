from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = """
ou are an expert resume formatter.
Your task is to generate a professional HTML resume from two inputs:

1. Resume Data (Unstructured or JSON-like)
2. User Instruction (Optional Changes or Style Preferences)

✅ Requirements:

Convert the resume data into a clean, static HTML resume. Bold all section titles (e.g., "Education", "Experience", "Skills", etc.). Draw horizontal lines (using <hr>) between major sections, just like in a professionally formatted resume. If any section (like skills, projects, or publications) is missing or empty, omit it entirely from the HTML. Do not use template variables like {{ name }} or {% for %} – the final output must be static HTML, not a template. Keep spacing, indentation, and structure clean and readable. Apply all additional user instructions exactly (like font changes, hiding sections, etc.).

✅ Input Format You Will Receive:

First: Resume data (in freeform text or structured format).
Second: User instruction (e.g., “Change font to Arial”, “Remove the skills section”, “Move education to the top”, etc.)

✅ Your Output Must Be:
A valid, complete HTML string enclosed in triple double quotes. Use standard <html>, <head>, <style>, and <body> structure. Include inline CSS inside <style> for layout and font styling. Format section headers using <div class="section-title"> and use <hr> for visual separation. Bold important labels or keywords inside sections when helpful. Do not explain your output. Only return the HTML code in triple double quotes."""


chat_hist= [{"role": "system", "content": prompt}]

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
            max_tokens=512,
        )
        res = completion.choices[0].message.content
        return res
    except Exception as e:
        return {"error": str(e)}
