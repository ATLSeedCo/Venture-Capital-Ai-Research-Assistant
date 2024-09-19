document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('researchForm');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const companyName = document.getElementById('companyName').value;
        const companyWebsite = document.getElementById('companyWebsite').value;

        // Show loading message and spinner
        loadingElement.style.display = 'block';
        loadingElement.innerHTML = '<p>Running Research Analysis</p><div class="spinner"></div>';
        resultsElement.innerHTML = '';

        // Send POST request to server
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'company_name': companyName,
                'company_website': companyWebsite
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Display results in HTML format
            if (data.analysis) {
                let analysisHtml = '<h2>Research Results:</h2>';
                for (const [key, value] of Object.entries(data.analysis)) {
                    analysisHtml += `<h3>${key}:</h3><p>${value}</p>`;
                }
                resultsElement.innerHTML = analysisHtml;
            } else {
                resultsElement.innerHTML = `<h2>Error:</h2><p>${data.error || 'Unknown error occurred'}</p>`;
            }
        })
        .catch(error => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Display detailed error message
            resultsElement.innerHTML = `<h2>Error:</h2><p>${error.message}</p>`;
            console.error('Error:', error);
        });
    });
});
