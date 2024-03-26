from nltk.corpus import stopwords

# Omkar Pathak
NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

# Education (Upper Case Mandatory)
EDUCATION = [
            'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E',
            'M.E.', 'MS', 'M.S', 'BTECH', 'MTECH',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'

NUMBER = r'\d+'

# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

STOPWORDS = set(stopwords.words('english'))

RESUME_SECTIONS_PROFESSIONAL = [
                    'experience',
                    'education',
                    'interests',
                    'professional experience',
                    'publications',
                    'skills',
                    'certifications',
                    'objective',
                    'career objective',
                    'summary',
                    'leadership'
                ]

RESUME_SECTIONS_GRAD = [
                    'accomplishments',
                    'experience',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                    'certifications',
                    'objective',
                    'career objective',
                    'summary',
                    'leadership'
                ]
job_titles = [
    "Cybersecurity Engineer", "Information Security Manager", "Security Architect",
    "Network Security Engineer", "Security Analyst", "Security Consultant",
    "Security Operations Manager", "Penetration Tester", "Ethical Hacker",
    "Incident Responder", "Security Auditor", "Cloud Security Engineer",
    "Identity and Access Management (IAM) Specialist", "Security Awareness Trainer",
    "DevSecOps Engineer", "Software Security Engineer", "Application Security Engineer",
    "Malware Analyst", "Forensic Analyst", "Threat Intelligence Analyst",
    "Security Compliance Analyst", "Privacy Officer", "Chief Information Security Officer (CISO)",
    "Chief Security Officer (CSO)", "Data Privacy Consultant", "Data Protection Officer (DPO)",
    "Network Engineer", "Systems Engineer", "IT Support Specialist",
    "Technical Support Engineer", "Help Desk Technician", "Desktop Support Engineer",
    "IT Administrator", "Systems Administrator", "Database Administrator",
    "Cloud Engineer", "Cloud Architect", "Cloud Solutions Architect",
    "Cloud Consultant", "Cloud Developer", "DevOps Engineer", "Site Reliability Engineer",
    "Release Engineer", "Build Engineer", "Automation Engineer", "Configuration Manager",
    "Continuous Integration/Continuous Delivery (CI/CD) Engineer", "Infrastructure Engineer",
    "Virtualization Engineer", "Containerization Engineer", "Network Administrator",
    "Systems Analyst", "Business Systems Analyst", "IT Business Analyst",
    "Data Analyst", "Database Developer", "Business Intelligence Developer",
    "ETL Developer", "Data Engineer", "Big Data Engineer", "Data Architect",
    "Business Intelligence Architect", "Data Warehouse Architect", "Machine Learning Engineer",
    "AI Engineer", "Computer Vision Engineer", "Natural Language Processing (NLP) Engineer",
    "Data Scientist", "Software Engineer", "Software Developer", "Web Developer",
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Mobile App Developer", "iOS Developer", "Android Developer",
    "Game Developer", "Embedded Systems Engineer", "Firmware Engineer",
    "Software Test Engineer", "Quality Assurance Engineer", "Automation Test Engineer",
    "Performance Test Engineer", "Security Test Engineer", "User Interface Designer",
    "User Experience Designer", "UI/UX Designer", "Interaction Designer",
    "Product Designer", "UX Researcher", "Usability Tester", "UI Developer",
    "UI Engineer", "UI Architect", "Systems Security Administrator",
    "Network Security Administrator", "Cybersecurity Administrator",
    "Database Security Administrator", "Web Security Administrator",
    "Security Software Developer", "Security Solutions Architect",
    "Cloud Security Architect", "Data Security Analyst", "Data Loss Prevention (DLP) Analyst",
    "Cybersecurity Operations Analyst", "Information Security Analyst",
    "Network Security Analyst", "Security Incident Response Analyst",
    "Threat Hunting Analyst", "Security Information and Event Management (SIEM) Analyst",
    "Vulnerability Management Analyst", "IT Auditor", "IT Compliance Analyst",
    "IT Risk Analyst", "Business Continuity Analyst", "Disaster Recovery Analyst",
    "IT Security Consultant", "Cybersecurity Consultant", "Information Security Consultant",
    "Security Policy Analyst", "Security Assurance Analyst", "Security Awareness Analyst",
    "Security Training Analyst", "Privacy Analyst", "Cloud Security Consultant",
    "Identity and Access Management (IAM) Consultant", "Network Security Consultant",
    "Infrastructure Consultant", "Software Consultant", "Technology Consultant",
    "Systems Integration Consultant", "Database Consultant", "Web Consultant",
    "Business Intelligence Consultant", "Data Management Consultant",
    "Project Manager", "IT Project Manager", "Technical Project Manager",
    "Infrastructure Project Manager", "Software Project Manager",
    "Agile Project Manager", "Scrum Master", "IT Service Manager",
    "IT Operations Manager", "IT Manager", "Technical Account Manager",
    "Solution Architect", "Technical Architect", "Enterprise Architect",
    "Infrastructure Architect", "Systems Architect", "Data Architect",
    "Database Architect", "Cloud Architect", "Security Architect",
    "Software Architect", "UI/UX Architect", "Network Architect",
    "DevOps Architect", "Quality Assurance Manager", "Software Development Manager",
    "Engineering Manager", "IT Director", "Technology Director",
    "Information Technology (IT) Director", "IT Vice President (IT VP)",
    "Chief Technology Officer (CTO)"
]
