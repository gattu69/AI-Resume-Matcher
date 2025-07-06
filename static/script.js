document.getElementById('analyze-btn').addEventListener('click', async () => {
    const resume = document.getElementById('resume').value;
    const jobDescription = document.getElementById('job_description').value;
    const resumeFile = document.getElementById('resume-upload').files[0];
    const jdFile = document.getElementById('jd-upload').files[0];

    if ((!resume && !resumeFile) || (!jobDescription && !jdFile)) {
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
        const formData = new FormData();
        formData.append('resume', resume);
        formData.append('job_description', jobDescription);
        if (resumeFile) formData.append('resume-upload', resumeFile);
        if (jdFile) formData.append('jd-upload', jdFile);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (!response.ok || data.error) {
            throw new Error(data.error || 'Server error');
        }

        document.getElementById('match-score').textContent = data.score;

        const matchingKeywordsContainer = document.getElementById('matching-keywords');
        matchingKeywordsContainer.innerHTML = data.matching_keywords
            .map(kw => `<span class="keyword match animate__animated animate__fadeIn">${kw}</span>`)
            .join('');

        const missingKeywordsContainer = document.getElementById('missing-keywords');
        missingKeywordsContainer.innerHTML = data.missing_keywords
            .map(kw => `<span class="keyword missing animate__animated animate__fadeIn">${kw}</span>`)
            .join('');

        const resumeAnalysisContainer = document.getElementById('resume-analysis');
        let analysisHtml = '';

        if (data.resume_analysis.sections) {
            analysisHtml += '<h4>Sections Found:</h4><ul>';
            for (const [section, items] of Object.entries(data.resume_analysis.sections)) {
                analysisHtml += `<li><strong>${section}:</strong> ${items.length} items</li>`;
            }
            analysisHtml += '</ul>';
        }

        if (data.resume_analysis.metrics) {
            analysisHtml += '<h4>Metrics:</h4><ul>';
            analysisHtml += `<li><strong>Word count:</strong> ${data.resume_analysis.metrics.word_count}</li>`;
            analysisHtml += `<li><strong>Bullet points:</strong> ${data.resume_analysis.metrics.bullet_points}</li>`;
            analysisHtml += `<li><strong>Action verbs:</strong> ${data.resume_analysis.metrics.action_verbs}</li>`;
            analysisHtml += '</ul>';
        }

        resumeAnalysisContainer.innerHTML = analysisHtml;

        const results = document.getElementById('results');
        results.classList.remove('hidden');
        results.classList.add('animate__fadeIn');

    } catch (error) {
        alert('Error analyzing match!\n' + error.message);
        console.error(error);
    } finally {
        btn.innerHTML = 'Analyze Match';
        btn.disabled = false;
    }
});

document.getElementById('resume-upload').addEventListener('change', function (e) {
    handleFileUpload(e, 'resume');
});

document.getElementById('jd-upload').addEventListener('change', function (e) {
    handleFileUpload(e, 'job_description');
});

function handleFileUpload(event, targetTextareaId) {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type === "application/pdf") {
        document.getElementById(targetTextareaId).value = "PDF file selected. Text will be extracted on server.";
    } else {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById(targetTextareaId).value = e.target.result;
        };
        reader.readAsText(file);
    }
}
