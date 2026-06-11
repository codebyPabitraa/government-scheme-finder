async function findSchemes() {
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const income = parseInt(document.getElementById('income').value);
    const caste = document.getElementById('caste').value;
    const state = document.getElementById('state').value;
    const occupation = document.getElementById('occupation').value;
    const extra = document.getElementById('extra').value;

    document.getElementById('loading').style.display = 'flex';
    document.getElementById('results-section').style.display = 'none';

    try {
        const response = await fetch('http://127.0.0.1:8000/find-schemes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ age, gender, income, caste, state, occupation, extra })
        });

        const data = await response.json();
        renderResults(data.result);
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        alert('Error connecting to server. Make sure backend is running.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function renderResults(text) {
    const container = document.getElementById('results-content');
    container.innerHTML = '';

    // Split by numbered schemes
    const lines = text.split('\n').filter(l => l.trim() !== '');
    let html = '';
    let inCard = false;

    for (let line of lines) {
        line = line.trim();

        // Numbered scheme line e.g. "1. **PM Kisan**:"
        if (/^\d+\.\s+\*\*/.test(line)) {
            if (inCard) html += '</div>';
            const title = line.replace(/^\d+\.\s+\*\*/, '').replace(/\*\*.*/, '').replace(/\*\*/g, '').trim();
            const fullTitle = line.replace(/^\d+\.\s+/, '').replace(/\*\*/g, '').trim();
            html += `
                <div class="scheme-card">
                    <div class="scheme-title">✅ ${fullTitle.replace(/:/g, '')}</div>
                    <div class="scheme-body">
            `;
            inCard = true;

        } else if (line.startsWith('**') && line.endsWith('**')) {
            // Bold standalone line
            html += `<p><strong>${line.replace(/\*\*/g, '')}</strong></p>`;

        } else if (line.startsWith('Please note') || line.startsWith('I recommend') || line.startsWith('As a') || line.startsWith('I hope')) {
            if (inCard) { html += '</div></div>'; inCard = false; }
            html += `<p class="note-text">💡 ${line}</p>`;

        } else {
            html += `<p>${line.replace(/\*\*/g, '<strong>').replace(/\*\*/g, '</strong>')}</p>`;
        }
    }

    if (inCard) html += '</div></div>';
    container.innerHTML = html;
}