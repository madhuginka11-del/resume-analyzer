from flask import Flask, render_template, request
import re
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os

app = Flask(__name__)

# 🔥 Skills list
COMMON_SKILLS = [
    "python","java","sql","machine learning","data science",
    "html","css","javascript","excel","deep learning"
]

# 🔥 Extract skills
def extract_skills(text):
    text = text.lower()
    found = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + skill + r'\b', text):
            found.append(skill)
    return found

# 🔥 Resume score
def calculate_score(skills):
    total_skills = 10
    score = int((len(skills) / total_skills) * 100)
    return min(score, 100)

# 🔥 Chart
def create_chart(skills):
    counts = {}
    for skill in skills:
        counts[skill] = counts.get(skill, 0) + 1

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.xticks(rotation=45)

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url

# 🔥 Job roles
JOB_ROLES = {
    "Data Scientist": ["python","machine learning","sql","data science"],
    "Web Developer": ["html","css","javascript"],
    "Data Analyst": ["excel","sql","python"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    results = []
    chart = None
    score = 0

    if request.method == "POST":
        resume = request.form["resume"]

        skills = extract_skills(resume)
        score = calculate_score(skills)
        chart = create_chart(skills)

        for job, req_skills in JOB_ROLES.items():
            matched = len(set(skills) & set(req_skills))
            total = len(req_skills)
            percent = int((matched / total) * 100)

            missing = list(set(req_skills) - set(skills))

            results.append({
                "job": job,
                "score": percent,
                "missing": missing
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", skills=skills, results=results, chart=chart, score=score)

# 🔥 Render fix
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
