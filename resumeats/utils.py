import docx
import PyPDF2
import re
from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

# Expanded keyword sets for different professions
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
    ]
}

def extract_text_from_resume(resume_file):
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
    score = 100
    feedback = []

    text_lower = text.lower()

    required_keywords = KEYWORDS.get(profession, [])
    found_keywords = [word for word in required_keywords if word.lower() in text_lower]
    missing_keywords = [word for word in required_keywords if word.lower() not in text_lower]

    if experience_level.lower() == "fresher":
        if len(found_keywords) < 7:
            feedback.append(f"As a fresher, consider including more relevant skills such as: {', '.join(missing_keywords[:10])}")
            score -= 20
    elif experience_level.lower() == "intermediate":
        if len(found_keywords) < 10:
            feedback.append(f"As an intermediate professional, your resume should highlight more technologies you've worked with. Consider adding: {', '.join(missing_keywords[:10])}")
            score -= 15
    else:  # Experienced
        if len(found_keywords) < 15:
            feedback.append(f"As an experienced professional, your resume should highlight more technologies you've worked with. Consider adding: {', '.join(missing_keywords[:10])}")
            score -= 20

    word_count = len(text.split())
    if experience_level.lower() == "fresher" and word_count < 300:
        feedback.append("Your resume is a bit short. Aim for at least 300 words to detail your education, projects, and skills.")
        score -= 10
    elif experience_level.lower() == "intermediate" and word_count < 400:
        feedback.append("Your resume should be more detailed. Aim for at least 400 words to cover your experience, projects, and skills.")
        score -= 10
    elif experience_level.lower() == "experienced" and word_count < 500:
        feedback.append("Your resume should be more detailed. Aim for at least 500 words to cover your work experience, projects, and skills.")
        score -= 10

    spell = SpellChecker()
    words = text.split()
    misspelled_words = spell.unknown(words)
    common_words = set(stopwords.words("english"))
    filtered_misspelled = [word for word in misspelled_words if word.lower() not in common_words]

    if filtered_misspelled:
        feedback.append(f"Possible spelling mistakes detected: {', '.join(filtered_misspelled[:5])}. Consider reviewing these words.")
        score -= 10

    essential_sections = ["education", "experience", "projects", "skills"]
    missing_sections = [section.capitalize() for section in essential_sections if section not in text_lower]

    if missing_sections:
        feedback.append(f"Your resume is missing the following sections: {', '.join(missing_sections)}. Including these sections can improve readability and completeness.")
        score -= 10

    if experience_level.lower() == "experienced":
        if "years of experience" not in text_lower:
            feedback.append("Specify your total years of experience to provide clarity on your professional background.")
            score -= 5

    score = max(score, 0)

    return score, "\n".join(feedback)
