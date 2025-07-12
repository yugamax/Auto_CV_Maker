from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = os.getenv("prompt")

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
