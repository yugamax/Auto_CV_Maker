import pdfplumber

def pdf_read():
    try:
        with pdfplumber.open(r"C:\Users\Aditya Prasad\Desktop\Harsh_Jain_Resume (1).pdf") as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

            # replacements = {
            #     "â€“": "-",
            #     "â€”": "-",
            #     "â€˜": "'",
            #     "â€™": "'",
            #     "â€œ": '"',
            #     "â€�": '"',
            #     "â€¦": "...",
            #     "âˆ™": "∙",
            #     "Â": "" }
            # for bad, good in replacements.items():
            #     full_text = full_text.replace(bad, good)

            print(full_text.strip())

    except Exception as e:
        print(f"Error reading PDF: {e}")

pdf_read()