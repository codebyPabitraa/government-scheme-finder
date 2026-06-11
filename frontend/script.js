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
        renderResults(data.result, data.links);
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        alert('Error connecting to server. Make sure backend is running.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function renderResults(text, links = []) {
    const container = document.getElementById('results-content');
    container.innerHTML = '';

    const schemeBlocks = text.split(/\n(?=\d+\.\s)/);

    let cardsHTML = '';
    let cardIndex = 0;

    schemeBlocks.forEach(block => {
        block = block.trim();
        if (!block) return;

        if (/^\d+\.\s/.test(block)) {
            const lines = block.split('\n').filter(l => l.trim());

            const titleLine = lines[0]
                .replace(/^\d+\.\s+/, '')
                .replace(/\*\*/g, '')
                .replace(/:$/, '')
                .trim();

            const summary = lines.slice(1)
                .map(l => l.replace(/\*\*/g, '').trim())
                .filter(l => l)
                .join(' ');

            // Use link by position, not by name
            const applyUrl = links[cardIndex] ? links[cardIndex].url : null;
            cardIndex++;

            cardsHTML += `
                <div class="scheme-card">
                    <div class="scheme-header">
                        <span class="scheme-icon">🏛️</span>
                        <h3 class="scheme-title">${titleLine}</h3>
                    </div>
                    ${summary ? `<p class="scheme-summary">${summary}</p>` : ''}
                    <div class="scheme-footer">
                        ${applyUrl
                            ? `<a href="${applyUrl}" target="_blank" class="apply-btn">Apply Now →</a>`
                            : `<a href="https://www.myscheme.gov.in" target="_blank" class="apply-btn">Apply Now →</a>`
                        }
                    </div>
                </div>
            `;
        } else {
            cardsHTML += `<p class="result-note">${block.replace(/\*\*/g, '')}</p>`;
        }
    });

    container.innerHTML = cardsHTML;
}
function findLink(title, linkMap) {
    const t = title.toLowerCase().trim();
    // Exact match
    if (linkMap[t]) return linkMap[t];
    // Partial match
    for (const key of Object.keys(linkMap)) {
        if (t.includes(key) || key.includes(t)) return linkMap[key];
    }
    return null;
}