import re
from collections import Counter
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import en_core_web_sm

nlp = en_core_web_sm.load()

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text

def extract_keywords(text, max_keywords=20):
    doc = nlp(text)
    keywords = []
    
    # Extract nouns and proper nouns
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
            keywords.append(token.lemma_)
    
    # Extract named entities
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'TECH']:
            keywords.append(ent.text.lower())
    
    # Count and get most common
    keyword_counts = Counter(keywords)
    return [kw for kw, count in keyword_counts.most_common(max_keywords)]

def calculate_match_score(resume_text, job_description_text):
    # Preprocess texts
    resume_processed = preprocess_text(resume_text)
    jd_processed = preprocess_text(job_description_text)
    
    # Extract keywords
    resume_keywords = extract_keywords(resume_processed)
    jd_keywords = extract_keywords(jd_processed)
    
    # Calculate matching keywords
    matching_keywords = set(resume_keywords) & set(jd_keywords)
    missing_keywords = set(jd_keywords) - set(resume_keywords)
    
    # TF-IDF similarity score
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_processed, jd_processed])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Convert to percentage
    match_score = round(similarity_score * 100, 1)
    
    return {
        'score': match_score,
        'missing_keywords': list(missing_keywords),
        'matching_keywords': list(matching_keywords)
    }

def analyze_resume(resume_text):
    doc = nlp(resume_text)
    
    # Extract sections
    sections = {
        'experience': [],
        'education': [],
        'skills': [],
        'summary': []
    }
    
    # Simple pattern matching for sections (real implementation would be more sophisticated)
    lines = resume_text.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.strip().lower()
        if 'experience' in line_lower or 'work history' in line_lower:
            current_section = 'experience'
        elif 'education' in line_lower:
            current_section = 'education'
        elif 'skills' in line_lower or 'technical skills' in line_lower:
            current_section = 'skills'
        elif 'summary' in line_lower or 'objective' in line_lower:
            current_section = 'summary'
        elif current_section and line.strip():
            sections[current_section].append(line.strip())
    
    # Count metrics
    word_count = len(resume_text.split())
    bullet_points = len([line for line in lines if line.strip().startswith('-') or line.strip().startswith('•')])
    action_verbs = len([token for token in doc if token.lemma_ in 
                       ['manage', 'lead', 'develop', 'create', 'implement', 'improve']])
    
    return {
        'sections': {k: v for k, v in sections.items() if v},
        'metrics': {
            'word_count': word_count,
            'bullet_points': bullet_points,
            'action_verbs': action_verbs
        }
    }