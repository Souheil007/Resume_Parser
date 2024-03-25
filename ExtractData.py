import utils

text = ""
pdf_path = './MY_CV.pdf'  

for extracted_text in utils.extract_text_from_pdf(pdf_path):
    text += extracted_text + "\n"
d = {"content": text}

print(d)
