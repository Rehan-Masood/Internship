// --- 1. LIVE INTERVIEW COUNTDOWN TIMER ---
let timeLeft = 45 * 60; // 45 minutes
const timerElem = document.getElementById('timer');

if (timerElem) {
    setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            const mins = Math.floor(timeLeft / 60);
            const secs = timeLeft % 60;
            timerElem.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }, 1000);
}

// --- 2. SAVE STRATEGY SCRATCHPAD NOTES ---
function saveNote(problemId) {
    const noteText = document.getElementById('noteInput').value;
    
    fetch('/api/save_note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem_id: problemId, note_text: noteText })
    })
    .then(res => res.json())
    .then(data => {
        const toastElem = document.getElementById('glassToast');
        if (toastElem) {
            const toast = new bootstrap.Toast(toastElem);
            toast.show();
        }
    })
    .catch(err => console.error("Error saving notes:", err));
}

// --- 3. DYNAMIC RANDOM CHALLENGE LOADER ---
function loadNextRandomChallenge() {
    fetch('/api/fetch_next_random_problem')
    .then(res => res.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch(err => console.error("Error fetching random problem:", err));
}

// --- 4. COPY REFERENCE SOLUTION TO EDITOR ---
function copySolutionToEditor() {
    const solutionText = document.getElementById('refSolutionText').textContent;
    const editor = document.getElementById('codeEditor');
    
    if (editor && solutionText) {
        editor.value = solutionText;
        
        // Hide solution modal cleanly
        const modalElem = document.getElementById('solutionModal');
        if (modalElem) {
            const modal = bootstrap.Modal.getInstance(modalElem);
            if (modal) {
                modal.hide();
            }
        }
    }
}

// --- 5. CODE EXECUTION & AUTO-PERSISTENCE OF PASSED SOLUTIONS ---
function executeCode(problemId) {
    const code = document.getElementById('codeEditor').value;
    const resultsContainer = document.getElementById('testCaseResults');
    const runBtn = document.getElementById('runBtn');
    const complexityBadge = document.getElementById('complexityBadge');

    resultsContainer.innerHTML = '<div class="text-cyan small"><i class="fa-solid fa-spinner fa-spin me-2"></i>Evaluating Python script against test cases...</div>';
    runBtn.disabled = true;

    fetch('/api/run_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code, problem_id: problemId })
    })
    .then(response => response.json())
    .then(data => {
        resultsContainer.innerHTML = '';

        // Display Complexity Analysis
        if (data.complexity && complexityBadge) {
            complexityBadge.textContent = data.complexity;
            complexityBadge.classList.remove('d-none');
        }

        // Render Test Case Evaluation Cards
        data.results.forEach(res => {
            const caseDiv = document.createElement('div');
            caseDiv.className = `p-2 mb-2 rounded border font-monospace small ${res.passed ? 'border-success bg-success-subtle text-success' : 'border-danger bg-danger-subtle text-danger'}`;
            caseDiv.innerHTML = `
                <div class="fw-bold">Case ${res.case}: ${res.passed ? 'PASSED ✅' : 'FAILED ❌'}</div>
                <div class="text-secondary small">Input: <code>${res.input}</code> | Expected: <code>${res.expected}</code> | Output: <code>${res.actual}</code></div>
            `;
            resultsContainer.appendChild(caseDiv);
        });

        // Show Success Indicator if all passed
        if (data.status === 'Passed') {
            const successNotice = document.createElement('div');
            successNotice.className = 'alert alert-success bg-success-subtle border-success text-success p-2 mt-2 small font-monospace fw-bold';
            successNotice.innerHTML = '<i class="fa-solid fa-circle-check me-2"></i>All test cases passed! Solution saved to your history.';
            resultsContainer.prepend(successNotice);
        }
    })
    .catch(err => {
        resultsContainer.innerHTML = '<div class="text-danger small"><i class="fa-solid fa-triangle-exclamation me-2"></i>Server Error: Could not evaluate code sandbox.</div>';
    })
    .finally(() => {
        runBtn.disabled = false;
    });
}