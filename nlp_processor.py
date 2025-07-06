# ----------------------
# nlp_processor.py
# ----------------------
import spacy
from collections import Counter
import re

nlp = spacy.load("en_core_web_sm")

action_verbs = [
    "achieved", "developed", "improved", "led", "managed", "created", "designed", "implemented",
    "increased", "reduced", "launched", "built", "analyzed", "negotiated", "organized"
]

def analyze_resume(text):
    doc = nlp(text)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_count = len(words)
    bullet_points = text.count("\u2022") + text.count("-")  # • and -

    found_verbs = [word for word in words if word in action_verbs]
    sections = {
        "Experience": re.findall(r"(?i)experience(.+?)(?=education|skills|projects|$)", text, re.DOTALL),
        "Education": re.findall(r"(?i)education(.+?)(?=experience|skills|projects|$)", text, re.DOTALL),
        "Skills": re.findall(r"(?i)skills(.+?)(?=experience|education|projects|$)", text, re.DOTALL),
        "Projects": re.findall(r"(?i)projects(.+?)(?=experience|skills|education|$)", text, re.DOTALL)
    }

    return {
        "metrics": {
            "word_count": word_count,
            "bullet_points": bullet_points,
            "action_verbs": len(set(found_verbs))
        },
        "sections": {k: v for k, v in sections.items() if v}
    }

def calculate_match_score(resume_text, jd_text):
    resume_doc = nlp(resume_text)
    jd_doc = nlp(jd_text)

    resume_tokens = [token.lemma_.lower() for token in resume_doc if not token.is_stop and not token.is_punct]
    jd_tokens = [token.lemma_.lower() for token in jd_doc if not token.is_stop and not token.is_punct]

    resume_counter = Counter(resume_tokens)
    jd_counter = Counter(jd_tokens)

    matching_keywords = [word for word in jd_counter if word in resume_counter]
    missing_keywords = [word for word in jd_counter if word not in resume_counter]

    score = round((len(matching_keywords) / max(1, len(jd_counter))) * 100, 2)

    return {
        "score": score,
        "matching_keywords": matching_keywords,
        "missing_keywords": missing_keywords
    }
