from flask import Flask, render_template, request, jsonify
from nlp_processor import analyze_resume, calculate_match_score
import PyPDF2
import os

app = Flask(__name__)

def extract_text_from_pdf(file_storage):
    try:
        file_storage.seek(0)
        reader = PyPDF2.PdfReader(file_storage)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip()
    except Exception as e:
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        resume_text = request.form.get('resume', '').strip()
        job_description = request.form.get('job_description', '').strip()

        # Handle uploaded resume
        resume_file = request.files.get('resume-upload')
        if resume_file and resume_file.filename:
            if resume_file.filename.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = resume_file.read().decode('utf-8', errors='ignore')

        # Handle uploaded job description
        jd_file = request.files.get('jd-upload')
        if jd_file and jd_file.filename:
            if jd_file.filename.lower().endswith('.pdf'):
                job_description = extract_text_from_pdf(jd_file)
            else:
                job_description = jd_file.read().decode('utf-8', errors='ignore')

        if not resume_text or not job_description:
            return jsonify({'error': 'Both resume and job description are required'}), 400

        resume_analysis = analyze_resume(resume_text)
        match_results = calculate_match_score(resume_text, job_description)

        return jsonify({
            'score': match_results['score'],
            'missing_keywords': match_results['missing_keywords'],
            'matching_keywords': match_results['matching_keywords'],
            'resume_analysis': resume_analysis
        })

    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
