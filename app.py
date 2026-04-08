from flask import Flask, render_template, request
from mymodel import extract_skills, match_jobs

app = Flask(__name__, static_folder="static")

@app.route("/", methods=["GET", "POST"])
def home():
    skills = []
    results = []
    avg_score = 0

    if request.method == "POST":
        resume = request.form["resume"]

        skills = extract_skills(resume)
        results = match_jobs(skills)

        if results:
            avg_score = sum([r["score"] for r in results]) // len(results)

    return render_template("index.html", skills=skills, results=results, avg_score=avg_score)

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
