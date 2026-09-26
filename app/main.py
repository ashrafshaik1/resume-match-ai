from parser import extract_text_from_pdf
from matcher import extract_skills


resume_path = "app/resumes/resume.pdf"
job_path = "app/job_descriptions/job.txt"

with open(job_path, "r") as file:
    job_text = file.read()

resume_text = extract_text_from_pdf(resume_path)

print("Extracted Resume Text:")
print(resume_text)

print("\nSkills Found:")

skills = extract_skills(resume_text)

for skill in skills:
    print("-", skill)

print("\nJob Required Skills:")

job_skills = extract_skills(job_text)

for skill in job_skills:
    print("-", skill)

matching_skills = set(skills) & set(job_skills)
missing_skills = set(job_skills) - set(skills)

match_percentage = (len(matching_skills) / len(job_skills)) * 100

print("\nMatching Skills:")

for skill in matching_skills:
    print("-", skill)

print("\nMissing Skills:")

for skill in missing_skills:
    print("-", skill)

print("\nMatch Percentage:")
print(round(match_percentage, 2), "%")