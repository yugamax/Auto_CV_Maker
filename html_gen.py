from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = """
You are an expert resume formatter.

Your task is to generate a clean, professional, and static HTML resume using two inputs:

1. Resume Data (Unstructured): Raw resume information provided by the user.
2. User Instructions (Optional): Any style preferences or custom formatting notes. If not provided, ignore.

✅ Requirements:

- Structure the resume into appropriate sections such as "Education", "Work Experience", "Projects", "Publications", "Leadership", and "Skills".
- Use proper HTML structure: <h1>, <h2>, <ul>, <li>, <p>, etc.
- Bold all section headings (e.g., "Education", "Experience", "Skills", etc.).
- Use only inline CSS for styling. Do not use any external CSS or JavaScript.
- Keep the layout clean and readable — suitable for a professional PDF export.
- Use bullet points for lists and group related items under the correct headings.
- Do not include any markdown, templating syntax, explanation, or code blocks.
- Return only the final HTML as raw text — no formatting or commentary.

Use the following styling and layout as reference:

- Page font: Georgia or Times New Roman
- Margin: 40px top/bottom, 60px left/right
- Font size: 12.5px body, 22px heading
- Section titles: Uppercase, bold, 14px
- Use horizontal lines between sections

Example of layout to follow:

<h1>HARSH JAIN</h1>
<p style="text-align: center; font-size: 11.5px;">New York, USA ∙ harshjain8445@gmail.com ∙ +91 8445728265 ∙ <a href="#">LinkedIn</a></p>

<h2 style="font-size:14px; font-weight:bold; margin-top:20px; text-transform:uppercase;">Education</h2>
<hr>
<ul>
  <li><strong>Columbia University</strong>, MS in Management Science and Engineering, 2025–2026</li>
  <li><strong>SRM Institute of Science and Technology</strong>, B.E., GPA: 8.74/10, 2021–2025</li>
</ul>

Repeat this clean structure for all sections.
"""


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
            max_tokens=2048,
        )
        res = completion.choices[0].message.content
        return res
    
    except Exception as e:
        print(f"Error generating resume: {e}")
        return {"error": str(e)}
