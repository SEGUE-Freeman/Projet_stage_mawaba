document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generator-form');
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');
    const resultsGrid = document.getElementById('results-grid');
    const successHeader = document.getElementById('success-header');
    
    // API CONFIG (Utilise l'URL absolue pour éviter les erreurs de fetch)
    const API_BASE_URL = 'http://127.0.0.1:8080/api';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Get Form Data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // 2. UI Transitions
        form.style.display = 'none';
        loading.style.display = 'block';
        submitBtn.disabled = true;

        try {
            // 3. API Call
            const response = await fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Erreur lors de la génération. Veuillez réessayer.');
            }

            const result = await response.json();
            const { project_id, links } = result;

            // 4. Update Result Links
            for (const key in links) {
                const linkElement = document.getElementById(`link-${key}`);
                if (linkElement) {
                    linkElement.href = links[key];
                }
            }

            // 5. Special Handling for Interactive HTML
            const iframe = document.getElementById('iframe-html');
            const iframeContainer = document.getElementById('iframe-container');
            if (links.html) {
                iframe.src = links.html;
                iframeContainer.style.display = 'block';
            }

            // 6. Show Results
            loading.style.display = 'none';
            successHeader.style.display = 'block';
            resultsGrid.style.display = 'grid';

        } catch (error) {
            console.error(error);
            alert(error.message);
            // Reset UI on error
            form.style.display = 'block';
            loading.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});
