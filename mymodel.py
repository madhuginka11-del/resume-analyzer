import pandas as pd

# 🔹 Load skills from file
def load_skills():
    with open("skills.txt", "r") as f:
        return f.read().splitlines()


# 🔹 Extract skills from resume text
def extract_skills(text):
    import re

    skills_list = load_skills()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    stopwords = ["i", "and", "know", "the", "is", "in", "of"]

    words = text.split()
    for word in words:
        if word not in stopwords:
            found.append(word)

    return list(set(found))

    # Match predefined skills
    for skill in skills_list:
        if skill in text:
            found.append(skill)

    # Also split words (to catch machine, learning, etc.)
    words = text.split()
    for word in words:
        found.append(word)

    return list(set(found))


# 🔹 Match jobs based on skills
def match_jobs(user_skills):
    df = pd.read_csv("jobs.csv")
    results = []

    user_skills = [s.lower() for s in user_skills]

    for _, row in df.iterrows():
        job_skills = row["skills"].lower().split()

        # ✅ Avoid duplicate counting
        matched_skills = set()

        for skill in user_skills:
            for js in job_skills:
                if skill in js or js in skill:
                    matched_skills.add(js)

        match = len(matched_skills)

        # ✅ Safe calculation (avoid division error)
        score = int((match / len(job_skills)) * 100) if len(job_skills) > 0 else 0

        missing = list(set(job_skills) - matched_skills)

        results.append({
            "job": row["job_title"],
            "score": score,
            "missing": missing
        })

    # Sort by highest score
    return sorted(results, key=lambda x: x["score"], reverse=True)