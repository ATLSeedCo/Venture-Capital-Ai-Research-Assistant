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
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Display results
            resultsElement.innerHTML = `<h2>Research Results:</h2><pre>${JSON.stringify(data, null, 2)}</pre>`;
        })
        .catch(error => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Display error message
            resultsElement.innerHTML = `<h2>Error:</h2><p>${error.message}</p>`;
        });
    });
});
