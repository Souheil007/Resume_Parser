#Annotations : Email Adress , Links , Skills , Graduation year , College Name , Degree , Companies worked at , Location , Name , Designation , Year Of experience
import utils

text = ""
pdf_path = './MY_CV.pdf'  # Or a BytesIO object if PDF is loaded into memory

for extracted_text in utils.extract_text_from_pdf(pdf_path):
    text += extracted_text + "\n"

# Assuming you wanted to store the text under the key "content" in dictionary d
d = {"content": text}
annotations=[]
utils.extract_email(text,annotations)
utils.extract_name(text,annotations)
'''
#Combine all annotations
data = {
    "content": content_text,
    "annotations": annotations
}

# Print or write the annotations to a file
print(data)'''
print(d)
print(annotations)
