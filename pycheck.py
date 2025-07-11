import pdfplumber

with pdfplumber.open(r"C:\Users\Aditya Prasad\Desktop\Harsh_Jain_Resume (1).pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()

print(text)