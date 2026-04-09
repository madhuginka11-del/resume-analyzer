from flask import Flask, render_template, request
from mymodel import extract_skills, match_jobs
import fitz  # PyMuPDF

app = Flask(__name__, static_folder="static")

# 🔥 PDF TEXT EXTRACTION
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text

@app.route("/", methods=["GET", "POST"])
def home():
    skills = []
    results = []
    avg_score = 0

    if request.method == "POST":

        file = request.files.get("resume_file")

        if file and file.filename.endswith(".pdf"):
            resume = extract_text_from_pdf(file)
        else:
            resume = request.form.get("resume", "")

        skills = extract_skills(resume)
        results = match_jobs(skills)

        if results:
            avg_score = sum([r["score"] for r in results]) // len(results)

    return render_template("index.html", skills=skills, results=results, avg_score=avg_score)

# 🔥 RENDER DEPLOY FIX
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))