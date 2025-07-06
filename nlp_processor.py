import spacy
from spacy.cli import download
from spacy.util import is_package
from collections import Counter
import re

# Automatically download en_core_web_sm if not installed
model_name = "en_core_web_sm"
if not is_package(model_name):
    download(model_name)

nlp = spacy.load(model_name)

action_verbs = ["developed", "designed", "implemented", "led", "created", "improved", "managed",
                "built", "analyzed", "resolved", "achieved", "organized", "supervised", "launched"]

def analyze_resume(resume_text):
    doc = nlp(resume_text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_count = len(tokens)
    bullet_points = len(re.findall(r"•|-", resume_text))
    action_verb_count = sum(resume_text.lower().count(verb) for verb in action_verbs)

    # Detect sections
    sections = {}
    current_section = None
    for line in resume_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.isupper() or line.endswith(":"):
            current_section = line.rstrip(":")
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)

    return {
        "metrics": {
            "word_count": word_count,
            "bullet_points": bullet_points,
            "action_verbs": action_verb_count
        },
        "sections": sections
    }

def calculate_match_score(resume_text, job_description):
    resume_doc = nlp(resume_text.lower())
    jd_doc = nlp(job_description.lower())

    resume_words = set(token.lemma_ for token in resume_doc if not token.is_stop and not token.is_punct)
    jd_words = set(token.lemma_ for token in jd_doc if not token.is_stop and not token.is_punct)

    matching_keywords = resume_words & jd_words
    missing_keywords = jd_words - resume_words

    score = round((len(matching_keywords) / len(jd_words)) * 100, 2) if jd_words else 0.0

    return {
        "score": score,
        "matching_keywords": sorted(matching_keywords),
        "missing_keywords": sorted(missing_keywords)
    }
