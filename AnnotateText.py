#Annotations : Email Adress , Links , Skills , Graduation year , College Name , Degree , Companies worked at , Location , Name , Designation(job title) , Year Of experience
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
utils.extract_skills(text,annotations)
utils.extract_links(text,annotations)
utils.extract_locations(text,annotations)
utils.extract_college_names(text,annotations)
utils.extract_experience(text,annotations)
utils.extract_degrees(text,annotations)
utils.extract_years_of_experience(text,annotations)
utils.extract_designations(text,annotations)


#Combine all annotations
data = {
    "content": text,
    "annotations": annotations
}
# Print or write the annotations to a file
print(data)

