from flask import Flask, render_template, request, jsonify
from nlp_processor import analyze_resume, calculate_match_score
import PyPDF2

app = Flask(__name__)

def extract_text_from_pdf(file_storage):
    file_storage.seek(0)  # Ensure pointer is at start
    reader = PyPDF2.PdfReader(file_storage)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get text from form fields
        resume_text = request.form.get('resume', '')
        job_description = request.form.get('job_description', '')

        # Check for file uploads and extract text if present
        if 'resume-upload' in request.files and request.files['resume-upload'].filename:
            file = request.files['resume-upload']
            file.seek(0)
            if file.filename.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf(file)
            else:
                resume_text = file.read().decode('utf-8', errors='ignore')

        if 'jd-upload' in request.files and request.files['jd-upload'].filename:
            file = request.files['jd-upload']
            file.seek(0)
            if file.filename.lower().endswith('.pdf'):
                job_description = extract_text_from_pdf(file)
            else:
                job_description = file.read().decode('utf-8', errors='ignore')

        if not resume_text.strip() or not job_description.strip():
            return jsonify({'error': 'Both resume and job description are required'}), 400

        resume_analysis = analyze_resume(resume_text)
        match_results = calculate_match_score(resume_text, job_description)

        response = {
            'score': match_results['score'],
            'missing_keywords': match_results['missing_keywords'],
            'matching_keywords': match_results['matching_keywords'],
            'resume_analysis': resume_analysis
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
