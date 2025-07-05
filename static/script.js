document.getElementById('analyze-btn').addEventListener('click', async () => {
    const resume = document.getElementById('resume').value;
    const jobDescription = document.getElementById('job_description').value;

    if (!resume || !jobDescription) {
        document.querySelectorAll('.input-box').forEach(box => {
            box.style.animation = 'rubberBand 0.8s';
            setTimeout(() => box.style.animation = '', 800);
        });
        return;
    }

    const btn = document.getElementById('analyze-btn');
    btn.innerHTML = '<span class="loader"></span> Analyzing...';
    btn.disabled = true;

    try {
        // Use FormData for sending as form data (not JSON)
        const formData = new FormData();
        formData.append('resume', resume);
        formData.append('job_description', jobDescription);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Server error');
        }

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('match-score').textContent = data.score;

        // Matching keywords
        const matchingKeywordsContainer = document.getElementById('matching-keywords');
        matchingKeywordsContainer.innerHTML = data.matching_keywords
            .map(kw => `<span class="keyword match animate__animated animate__fadeIn">${kw}</span>`)
            .join('');

        // Missing keywords
        const missingKeywordsContainer = document.getElementById('missing-keywords');
        missingKeywordsContainer.innerHTML = data.missing_keywords
            .map(kw => `<span class="keyword missing animate__animated animate__fadeIn">${kw}</span>`)
            .join('');

        // Resume analysis
        const resumeAnalysisContainer = document.getElementById('resume-analysis');
        let analysisHtml = '';

        // Sections
        if (data.resume_analysis.sections) {
            analysisHtml += '<h4>Sections Found:</h4><ul>';
            for (const [section, items] of Object.entries(data.resume_analysis.sections)) {
                analysisHtml += `<li class="animate__animated animate__fadeIn"><strong>${section}:</strong> ${items.length} items</li>`;
            }
            analysisHtml += '</ul>';
        }

        // Metrics
        if (data.resume_analysis.metrics) {
            analysisHtml += '<h4>Metrics:</h4><ul>';
            analysisHtml += `<li class="animate__animated animate__fadeIn"><strong>Word count:</strong> ${data.resume_analysis.metrics.word_count}</li>`;
            analysisHtml += `<li class="animate__animated animate__fadeIn"><strong>Bullet points:</strong> ${data.resume_analysis.metrics.bullet_points}</li>`;
            analysisHtml += `<li class="animate__animated animate__fadeIn"><strong>Action verbs:</strong> ${data.resume_analysis.metrics.action_verbs}</li>`;
            analysisHtml += '</ul>';
        }

        resumeAnalysisContainer.innerHTML = analysisHtml;

        // Show results
        const results = document.getElementById('results');
        results.classList.remove('hidden');
        results.classList.add('animate__fadeIn');

    } catch (error) {
        alert('Error analyzing match!');
        console.error(error);
    } finally {
        btn.innerHTML = 'Analyze Match';
        btn.disabled = false;
    }
});

// Handle file uploads (keep your existing code)
document.getElementById('resume-upload').addEventListener('change', function(e) {
    handleFileUpload(e, 'resume');
});

document.getElementById('jd-upload').addEventListener('change', function(e) {
    handleFileUpload(e, 'job_description');
});

function handleFileUpload(event, targetTextareaId) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById(targetTextareaId).value = e.target.result;
    };
    reader.readAsText(file);
}