
import io
import os
import re
import nltk
import utils
import pandas as pd
import docx2txt
from datetime import datetime
from dateutil import relativedelta
import constants as cs
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
def extract_name(text, annotations):
    import spacy
    from spacy.matcher import Matcher
    
    # Load English language model
    nlp = spacy.load("en_core_web_sm")

    # Define the NAME_PATTERN
    # Define a pattern to match: proper noun followed by a proper noun
    NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    # Initialize Matcher
    matcher = Matcher(nlp.vocab)

    # Add the pattern to the Matcher
    matcher.add('NAME',[NAME_PATTERN])

    # Process the text
    doc = nlp(text)  #t9assamlek el text el tokens

    # Perform matching
    matches = matcher(doc)

    # Extract matched names
    matched_names = []

    for _, start, end in matches:
        '''if 'name' not in span.text.lower():
            return span.text'''
        span = doc[start:end]
        if span.start == 0 or doc[span.start - 1].is_sent_start:
            name_text = span.text
            name_dict = {
                "label": ["Name"],
                "points": [{
                    "start": span.start_char,
                    "end": span.end_char,
                    "text": name_text
                }]
            }
            annotations.append(name_dict)
text = ""
pdf_path = './MY_CV.pdf'  # Or a BytesIO object if PDF is loaded into memory

for extracted_text in utils.extract_text_from_pdf(pdf_path):
    text += extracted_text + "\n"

# Assuming you wanted to store the text under the key "content" in dictionary d
d = {"content": text}
annotations=[]
