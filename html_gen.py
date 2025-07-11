from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

prompt = ""
chat_hist= [{"role": "system", "content": prompt}]

def gen_res(text, prompt=""):
    global chat_hist
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_hist,
            temperature=0.2,
            max_tokens=512,
        )

        res = completion.choices[0].message.content
        return res

    except Exception as e:
        return {"error": str(e)}
