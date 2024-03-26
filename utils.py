import io
import os
import re
import nltk
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
nltk.download('wordnet')


def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    '''
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    if not isinstance(pdf_path, io.BytesIO):
        # extract text from local pdf file
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        codec='utf-8',
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:
        # extract text from remote pdf file
        try:
            for page in PDFPage.get_pages(
                    pdf_path,
                    caching=True,
                    check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,
                    codec='utf-8',
                    laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield {"content": text} 

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return


def get_number_of_pages(file_name):
    try:
        if isinstance(file_name, io.BytesIO):
            # for remote pdf file
            count = 0
            for page in PDFPage.get_pages(
                        file_name,
                        caching=True,
                        check_extractable=True
            ):
                count += 1
            return count
        else:
            # for local pdf file
            if file_name.endswith('.pdf'):
                count = 0
                with open(file_name, 'rb') as fh:
                    for page in PDFPage.get_pages(
                            fh,
                            caching=True,
                            check_extractable=True
                    ):
                        count += 1
                return count
            else:
                return None
    except PDFSyntaxError:
        return None


def extract_text_from_docx(doc_path):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    try:
        temp = docx2txt.process(doc_path)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' '


def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc files

    :param doc_path: path to .doc file to be extracted
    :return: string of extracted text
    '''
    try:
        try:
            import textract
        except ImportError:
            return ' '
        text = textract.process(doc_path).decode('utf-8')
        return text
    except KeyError:
        return ' '


def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == '.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page
    elif extension == '.docx':
        text = extract_text_from_docx(file_path)
    elif extension == '.doc':
        text = extract_text_from_doc(file_path)
    return text


def extract_entity_sections_grad(text):
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for graduates and undergraduates

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1: #(potentially indicating a section header).
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS_GRAD)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS_GRAD:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)

    # entity_key = False
    # for entity in entities.keys():
    #     sub_entities = {}
    #     for entry in entities[entity]:
    #         if u'\u2022' not in entry:
    #             sub_entities[entry] = []
    #             entity_key = entry
    #         elif entity_key:
    #             sub_entities[entity_key].append(entry)
    #     entities[entity] = sub_entities

    # pprint.pprint(entities)

    # make entities that are not found None
    # for entity in cs.RESUME_SECTIONS:
    #     if entity not in entities.keys():
    #         entities[entity] = None
    return entities


def extract_entities_wih_custom_model(custom_nlp_text):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text: object of `spacy.tokens.doc.Doc`
    :return: dictionary of entities
    '''
    entities = {}
    for ent in custom_nlp_text.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
    for key in entities.keys():
        entities[key] = list(set(entities[key]))
    return entities


def get_total_experience(experience_list):
    '''
    Wrapper function to extract total months of experience from a resume

    :param experience_list: list of experience text extracted
    :return: total months of experience
    '''
    exp_ = []
    for line in experience_list:
        experience = re.search(
            r'(?P<fmonth>\w+.\d+)\s*(\D|to)\s*(?P<smonth>\w+.\d+|present)',
            line,
            re.I
        )
        if experience:
            exp_.append(experience.groups())
    total_exp = sum(
        [get_number_of_months_from_dates(i[0], i[2]) for i in exp_]
    )
    total_experience_in_months = total_exp
    return total_experience_in_months


def get_number_of_months_from_dates(date1, date2):
    '''
    Helper function to extract total months of experience from a resume

    :param date1: Starting date
    :param date2: Ending date
    :return: months of experience from date1 to date2
    '''
    if date2.lower() == 'present':
        date2 = datetime.now().strftime('%b %Y')
    try:
        if len(date1.split()[0]) > 3:
            date1 = date1.split()
            date1 = date1[0][:3] + ' ' + date1[1]
        if len(date2.split()[0]) > 3:
            date2 = date2.split()
            date2 = date2[0][:3] + ' ' + date2[1]
    except IndexError:
        return 0
    try:
        date1 = datetime.strptime(str(date1), '%b %Y')
        date2 = datetime.strptime(str(date2), '%b %Y')
        months_of_experience = relativedelta.relativedelta(date2, date1)
        months_of_experience = (months_of_experience.years
                                * 12 + months_of_experience.months)
    except ValueError:
        return 0
    return months_of_experience


def extract_entity_sections_professional(text):
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for professionals

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) \
                    & set(cs.RESUME_SECTIONS_PROFESSIONAL)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS_PROFESSIONAL:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    return entities


def extract_email(text,annotations):
    #email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    for email in emails:
        annotations.append({
            "label": ["Email Address"],
            "points": [{
                "start": text.find(email),
                "end": text.find(email) + len(email),
                "text": email
            }]
        })
    '''if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None'''

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


def extract_mobile_number(text, custom_regex=None):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    # Found this complicated regex on :
    # https://zapier.com/blog/extract-links-email-phone-regex/
    # mob_num_regex = r'''(?:(?:\+?([1-9]|[0-9][0-9]|
    #     [0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|
    #     [2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|
    #     [0-9]1[02-9]|[2-9][02-8]1|
    #     [2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|
    #     [2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{7})
    #     (?:\s*(?:#|x\.?|ext\.?|
    #     extension)\s*(\d+))?'''
    if not custom_regex:
        mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
        phone = re.findall(re.compile(mob_num_regex), text)
    else:
        phone = re.findall(re.compile(custom_regex), text)
    if phone:
        number = ''.join(phone[0])
        return number


def extract_skills(text, annotations, skills_file=None):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop]
    if not skills_file:
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'skills.csv')
        )
    else:
        data = pd.read_csv(skills_file)
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    noun_chunks=[chunk.text.lower().strip() for chunk in doc.noun_chunks]
    #he4a ilemmlek koll kelmtin mab3a4hom wi9arenhom bel les skills
    for i in range(len(noun_chunks) - 1):
        bi_gram = ' '.join(noun_chunks[i:i+2])
        if bi_gram in skills:
            skillset.append(bi_gram)
    
    #he4a ilemmlek koll 3 kelmet mab3a4hom wi9arenhom bel les skills
    for i in range(len(noun_chunks) - 2):
        tri_gram = ' '.join(noun_chunks[i:i+3])
        if tri_gram in skills:
            skillset.append(tri_gram)
    
    for skill in skillset:
        annotations.append({
            "label": ["Skills"],
            "points": [{
                "start": text.find(skill),
                "end": text.find(skill) + len(skill),
                "text": skill
            }]
        })
def extract_links(text, annotations):
    # Define the pattern to match URLs
    url_pattern = r'https?://\S+|www\.\S+'

    # Find all matches of URLs in the text
    urls = re.findall(url_pattern, text)

    # Extract matched URLs
    for url in urls:
        annotations.append({
            "label": ["Link"],
            "points": [{
                "start": text.find(url),
                "end": text.find(url) + len(url),
                "text": url
            }]
        })

def extract_graduation_year(text, annotations):
    import spacy
    from spacy.matcher import Matcher
    # Load English language model
    nlp = spacy.load("en_core_web_sm")

    # Define patterns to match graduation years
    # Example: "graduated in 2010", "graduation year: 2005", "graduated in the year 2022"
    YEAR_PATTERNS = [
        [{"LOWER": {"in", "year", "on"}}, {"SHAPE": "dddd"}],  # e.g., "in 2010", "year 2005"
        [{"LOWER": "graduated"}, {"LOWER": "in"}, {"SHAPE": "dddd"}],  # e.g., "graduated in 2010"
        [{"LOWER": "graduation"}, {"LOWER": "year"}, {"IS_DIGIT": True, "LENGTH": 4}]  # e.g., "graduation year: 2005"
    ]

    # Initialize Matcher
    matcher = Matcher(nlp.vocab)

    # Add the patterns to the Matcher
    for pattern in YEAR_PATTERNS:
        matcher.add('YEAR', [pattern])

    # Process the text
    doc = nlp(text)

    # Perform matching
    matches = matcher(doc)

    # Extract matched graduation years
    for _, start, end in matches:
        span = doc[start:end]
        graduation_year_text = span.text
        year_dict = {
            "label": ["Graduation_Year"],
            "points": [{
                "start": span.start_char,
                "end": span.end_char,
                "text": graduation_year_text
            }]
        }
        annotations.append(year_dict)           

def extract_degrees(resume_text, annotations):
    # Define patterns to match degree names
    degree_patterns = [
        r"(?i)\b(bachelor|b\.?s\.?|bachelor's)\b",
        r"(?i)\b(master|ms|m\.?s\.?|master's)\b",
        r"(?i)\b(doctorate|ph\.?d\.?|doctor's|phd)\b",
        # Add more patterns as needed
    ]

    # Find all matches of degree patterns in the text
    matches = []
    for pattern in degree_patterns:
        matches.extend(re.findall(pattern, resume_text))

    # Extract matched degree names
    for degree in matches:
        degree_dict = {
            "label": ["Degree"],
            "points": [{
                "start": resume_text.lower().index(degree.lower()),
                "end": resume_text.lower().index(degree.lower()) + len(degree),
                "text": degree
            }]
        }
        annotations.append(degree_dict)

def extract_locations(text, annotations):
    import spacy
    # Load English language model with NER
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Extract locations
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE stands for geopolitical entity
            location_dict = {
                "label": ["Location"],
                "points": [{
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "text": ent.text
                }]
            }
            annotations.append(location_dict)

def extract_college_names(text, annotations):
    import spacy
    # Load English language model with NER
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Extract college names
    for ent in doc.ents:
       #if ent.label_ == "ORG" or ent.label_ == "EDU":  # ORG for organization, EDU for educational institution
        if ent.label_ == "EDU":  # ORG for organization, EDU for educational institution
            college_name_dict = {
                "label": ["College_Name"],
                "points": [{
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "text": ent.text
                }]
            }
            annotations.append(college_name_dict)
            
def extract_years_of_experience(resume_text, annotations):
    # Define patterns to match years of experience
    experience_patterns = [
        r"\b(\d+)\s*years?(\s*\d+\s*months?)?\b",  # Matches "5 years", "3 years 6 months", etc.
        # Add more patterns as needed
    ]

    # Find all matches of experience patterns in the text
    matches = []
    for pattern in experience_patterns:
        matches.extend(re.findall(pattern, resume_text))

    # Extract matched years of experience
    for match in matches:
        years_of_experience = match[0] if match[0] else "0"  # Extract years if present, otherwise default to "0"
        months_of_experience = match[1] if len(match) > 1 and match[1] else "0"  # Extract months if present, otherwise default to "0"
        total_months_of_experience = int(years_of_experience) * 12 + int(months_of_experience)

        experience_dict = {
            "label": ["Year Of experience"],
            "points": [{
                "start": resume_text.lower().index(match[0]),
                "end": resume_text.lower().index(match[0]) + len(match[0]),
                "text": f"{years_of_experience} years {months_of_experience} months"
            }]
        }
        annotations.append(experience_dict)
        


def extract_designations(resume_text, annotations):#job titles
    # Predefined list of job titles
    # Compile regular expression pattern to match job titles
    pattern = r'\b(?:' + '|'.join(re.escape(title) for title in cs.job_titles) + r')\b'

    # Find all matches of job titles in the text
    matches = re.findall(pattern, resume_text, flags=re.IGNORECASE)

    # Extract matched job titles
    for match in matches:
        designation_dict = {
            "label": ["Designation"],
            "points": [{
                "start": resume_text.lower().index(match.lower()),
                "end": resume_text.lower().index(match.lower()) + len(match),
                "text": match
            }]
        }
        annotations.append(designation_dict)
'''
def cleanup(token, lower=True):
    if lower:
        token = token.lower()
    return token.strip()
'''
'''
#hna te5dem bdes educations tfixihom enti
def extract_education(nlp_text):
    edu = {}
    # Extract education degree
    try:
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
    except IndexError:
        pass

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education
'''


def extract_companies(resume_text, annotations):
    import spacy
    # Load English language model with NER
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(resume_text)

    # Extract companies
    for ent in doc.ents:
        if ent.label_ == "ORG":
            company_dict = {
                "label": ["Companies worked at"],
                "points": [{
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "text": ent.text
                }]
            }
            annotations.append(company_dict)
def extract_experience(resume_text, annotations):
    import nltk
    
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize
    filtered_sentence = [
        w for w in word_tokens if w.lower() not in stop_words and wordnet_lemmatizer.lemmatize(w.lower()) not in stop_words
    ]
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)

    # Extract phrases
    phrases = []
    for vp in list(cs.subtrees(filter=lambda x: x.label() == 'P')):
        phrase = " ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2])
        phrases.append(phrase)

    # Search for 'experience' in the phrases and extract the text after it
    experiences = [
        phrase[phrase.lower().index('experience') + 10:].strip()
        for phrase in phrases
        if phrase and 'experience' in phrase.lower()
    ]

    # Append extracted experiences to annotations
    for experience in experiences:
        experience_dict = {
            "label": ["Experience"],
            "points": [{
                "start": resume_text.lower().index('experience') + 10,
                "end": resume_text.lower().index('experience') + 10 + len(experience),
                "text": experience
            }]
        }
        annotations.append(experience_dict)