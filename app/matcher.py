import re

SKILL_ALIASES = {
    "python": [
        "python",
        "python programming",
        "python developer",
        "python development"
    ],

    "java": [
        "java",
        "java programming",
        "java developer"
    ],

    "c": [
        "c programming",
        "c language"
    ],

    "c++": [
        "c++",
        "cpp",
        "c plus plus"
    ],

    "sql": [
        "sql",
        "sql programming",
        "structured query language"
    ],

    "html": [
        "html",
        "html5"
    ],

    "css": [
        "css",
        "css3"
    ],

    "javascript": [
        "javascript",
        "java script",
        "js"
    ],

    "react": [
        "react",
        "react.js",
        "reactjs"
    ],

    "angular": [
        "angular",
        "angular.js",
        "angularjs"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "spring boot": [
        "spring boot",
        "springboot"
    ],

    "django": [
        "django",
        "django framework"
    ],

    "flask": [
        "flask",
        "flask framework"
    ],

    "git": [
        "git",
        "git version control"
    ],

    "github": [
        "github",
        "git hub"
    ],

    "docker": [
        "docker",
        "docker container",
        "containerization"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "machine learning": [
        "machine learning",
        "ml",
        "machine learning algorithms"
    ],

    "deep learning": [
        "deep learning",
        "dl",
        "deep learning algorithms"
    ],

    "pandas": [
        "pandas",
        "python pandas"
    ],

    "numpy": [
        "numpy",
        "python numpy"
    ]
}


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            # Special handling for C
            if skill == "c":
                pattern = r"(?<!\w)c(?![\w+#])"

            # Special handling for C++
            elif skill == "c++":
                if alias == "c++":
                    pattern = r"(?<!\w)c\+\+(?!\w)"
                else:
                    pattern = r"\b" + re.escape(alias) + r"\b"

            # All other skills
            else:
                pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return sorted(found_skills)

def compare_skills(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matching_skills = sorted(resume_set.intersection(job_set))
    missing_skills = sorted(job_set - resume_set)

    if len(job_set) == 0:
        match_percentage = 0
    else:
        match_percentage = (len(matching_skills) / len(job_set)) * 100

    return matching_skills, missing_skills, match_percentage