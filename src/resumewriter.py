from common import get_model

model = get_model()

TEMPLATE = """You are an expert resume writer. Create an ATS-friendly, one-page resume for:
Name: {name}
Target Role: {job_title}
Experience Summary (bullet-style): {experience}
Skills (comma separated): {skills}
Education: {education}

Requirements:
- Clean headings: SUMMARY, SKILLS, EXPERIENCE, EDUCATION
- Use strong action verbs and quantifiable achievements
- Avoid tables, images, colors
- Keep it concise and skimmable
"""

def generate_resume(name, job_title, skills, experience, education):
    prompt = TEMPLATE.format(
        name=name,
        job_title=job_title,
        skills=skills,
        experience=experience,
        education=education
    )
    return model.generate_content(prompt).text

def app():
    print("📄 Resume Writer")
    name = input("Name: ").strip()
    job_title = input("Target Role (e.g., Prompt Engineer): ").strip()
    skills = input("Skills (comma separated): ").strip()
    experience = input("Experience summary (bullets; use semicolons to separate): ").strip()
    education = input("Education (e.g., B.Tech CSE, 2018): ").strip()

    resume = generate_resume(name, job_title, skills, experience, education)
    print("\n--- GENERATED RESUME ---\n")
    print(resume)

if __name__ == "__main__":
    app()