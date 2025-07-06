import spacy.cli
spacy.cli.download("en_core_web_sm")
import spacy
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
from flask import Flask, render_template, request, jsonify
from nlp_processor import analyze_resume, calculate_match_score
import os

nlp = en_core_web_sm.load()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        resume_text = request.form['resume']
        job_description = request.form['job_description']
        
        if not resume_text or not job_description:
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
