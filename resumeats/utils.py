import docx
import PyPDF2
import re
from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

# Essential sections required in a resume
ESSENTIAL_SECTIONS = ["education", "experience", "projects", "skills"]
COMMON_KEYWORDS = ["certifications", "technical skills", "programming languages", "achievements"]

# Profession-based keywords
KEYWORDS = {
    "Python Backend": [
        "Python", "Django", "Flask", "FastAPI", "REST API", "GraphQL", "SQL",
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Celery", "Docker",
        "Kubernetes", "CI/CD", "Git", "ORM", "AsyncIO", "Microservices",
        "Design Patterns", "Unit Testing", "Logging", "Authentication",
        "Authorization", "AWS", "Cloud Computing", "Security", "API Gateway"
    ],
    "Frontend": [
        "React", "JavaScript", "TypeScript", "CSS", "HTML", "Tailwind",
        "Redux", "Next.js", "Vue.js", "Webpack", "Babel", "Jest",
        "Cypress", "GraphQL", "APIs", "Component-Based", "State Management",
        "SSR", "Client-Side Rendering", "WebSockets", "PWA", "Figma",
        "UI/UX", "Animation", "Lazy Loading", "Performance Optimization"
    ],
    "Java Backend": [
        "Java", "Spring Boot", "Hibernate", "JPA", "REST API", "SOAP", "SQL",
        "PostgreSQL", "MySQL", "MongoDB", "JVM", "Maven", "Gradle", "JUnit",
        "Microservices", "CI/CD", "Git", "Docker", "Kubernetes", "AWS"
    ],
    "Data Science": [
        "Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "Matplotlib",
        "Seaborn", "SQL", "Machine Learning", "Deep Learning", "Data Visualization",
        "Statistics", "Big Data", "Hadoop", "Spark", "Data Cleaning", "Model Evaluation"
    ],
    "PHP": [
        "PHP", "Laravel", "Symfony", "MySQL", "PostgreSQL", "REST API", "Git",
        "Composer", "MVC", "OOP", "HTML", "CSS", "JavaScript", "jQuery", "AJAX", "MySQL"
    ],
     "AI & ML": [
        "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow",
        "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy", "SciPy",
        "Natural Language Processing", "Computer Vision", "Model Training",
        "Data Preprocessing", "Hyperparameter Tuning", "Pipeline", "API Deployment",
        "AWS SageMaker", "Google AI Platform", "Model Evaluation", "Data Visualization"
    ],

    "Full Stack": [
        "JavaScript", "Node.js", "Express", "React", "Angular", "Vue.js",
        "HTML5", "CSS3", "Bootstrap", "Tailwind CSS", "REST API", "GraphQL",
        "MongoDB", "PostgreSQL", "MySQL", "Django", "Flask", "Docker", "Kubernetes",
        "CI/CD", "Git", "Webpack", "Babel", "Authentication", "Authorization"
    ]

}

def extract_text_from_resume(resume_file):
    """Extract text from a PDF or DOCX resume."""
    text = ""

    if resume_file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(resume_file)
            text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        except Exception as e:
            return None, "Error reading PDF file"

    elif resume_file.name.endswith(".docx"):
        try:
            doc = docx.Document(resume_file)
            text = " ".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return None, "Error reading DOCX file"

    else:
        return None, "Unsupported file format. Please upload PDF or DOCX."

    return text, None

def analyze_resume(text, profession, experience_level):
    """Analyze resume for missing sections, keywords, spelling errors, and word count."""
    text_lower = text.lower()
    feedback = []
    score = 100


    if not any(section in text_lower for section in ESSENTIAL_SECTIONS):
        return 0, "This does not seem to be a resume. Ensure it includes sections like Education, Experience, Skills, and Projects."


    missing_sections = [sec.capitalize() for sec in ESSENTIAL_SECTIONS if sec not in text_lower]
    if missing_sections:
        feedback.append(f"Missing sections: {', '.join(missing_sections)}.")
        score -= 12

  
    missing_common = [word.capitalize() for word in COMMON_KEYWORDS if word not in text_lower]
    if missing_common:
        feedback.append(f"Consider adding: {', '.join(missing_common)}.")
        score -= 6

  
    required_keywords = KEYWORDS.get(profession, [])
    found_keywords = [word for word in required_keywords if word.lower() in text_lower]
    missing_keywords = [word for word in required_keywords if word.lower() not in text_lower]

    if experience_level.lower() == "fresher" and len(found_keywords) < 7:
        feedback.append(f"Consider adding more skills: {', '.join(missing_keywords[:5])}.")
        score -= 11
    elif experience_level.lower() == "intermediate" and len(found_keywords) < 10:
        feedback.append(f"Your resume could include more skills: {', '.join(missing_keywords[:5])}.")
        score -= 15
    elif experience_level.lower() == "experienced" and len(found_keywords) < 15:
        feedback.append(f"Consider including more advanced skills: {', '.join(missing_keywords[:5])}.")
        score -= 20


    word_count = len(text.split())
    min_word_count = {"fresher": 50, "intermediate": 100, "experienced": 150}
    if word_count < min_word_count.get(experience_level.lower(), 150):
        feedback.append(f"Resume is too short ({word_count} words). Consider adding more details.")
        score -= 9

   
    spell = SpellChecker()
    words = text.split()
    misspelled_words = spell.unknown(words)
    common_words = set(stopwords.words("english"))
    filtered_misspelled = [word for word in misspelled_words if word.lower() not in common_words]

    if filtered_misspelled:
        feedback.append(f"Possible spelling mistakes: {', '.join(filtered_misspelled[:5])}.")
        score -= 10

    # Ensure score is not negative
    score = max(score, 0)

    return score, "\n".join(feedback)

