from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = """
You are an expert resume formatter.

Your task is to generate a clean, professional, and static HTML resume using two inputs:

1. **Resume Data (Unstructured)** – Raw resume information without formatting.
2. **User Instructions (Optional)** – Any specific style preferences or changes requested. If not provided, ignore.

✅ **Requirements:**

- Parse and structure the unformatted resume data into a static HTML resume.
- Bold all section titles (e.g., "Education", "Experience", "Skills", etc.).
- Do **not** include any JavaScript, external CSS, or frameworks. Use **only inline CSS** for styling.
- Maintain a clean, readable layout suitable for professional use.
- **Output only the final HTML** — no explanation, no formatting tips, no markdown, and no code blocks.

Use the following static HTML template as a structural and stylistic reference:

```html
<!-- resume_template.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ name }} - Resume</title>
    <style>
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            margin: 40px 60px;
            font-size: 12.5px;
            line-height: 1.6;
            color: #000;
        }
        h1 {
            font-size: 22px;
            text-align: center;
            margin-bottom: 0;
        }
        .contact {
            text-align: center;
            font-size: 11.5px;
            margin-bottom: 20px;
        }
        hr {
            border: none;
            border-top: 1px solid #000;
            margin: 8px 0;
        }
        .section-title {
            font-weight: bold;
            font-size: 14px;
            margin-top: 20px;
            text-transform: uppercase;
        }
        ul {
            margin-top: 4px;
            padding-left: 18px;
        }
        li {
            margin-bottom: 3px;
        }
    </style>
</head>
<body>

<h1>{{ name }}</h1>
<div class="contact">
    {{ email }} ∙ {{ phone }} ∙ <a href="{{ linkedin }}">{{ linkedin }}</a>
</div>

<div class="section-title">Education</div>
<hr>
<ul>
    {% for edu in education %}
        <li>{{ edu }}</li>
    {% endfor %}
</ul>

<div class="section-title">Experience</div>
<hr>
<ul>
    {% for exp in experience %}
        <li>{{ exp }}</li>
    {% endfor %}
</ul>

<div class="section-title">Projects</div>
<hr>
<ul>
    {% for proj in projects %}
        <li>{{ proj }}</li>
    {% endfor %}
</ul>

<div class="section-title">Skills</div>
<hr>
<ul>
    {% for skill in skills %}
        <li>{{ skill }}</li>
    {% endfor %}
</ul>

</body>
</html>

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
            max_tokens=512,
        )
        res = completion.choices[0].message.content
        return res
    
    except Exception as e:
        print(f"Error generating resume: {e}")
        return {"error": str(e)}
