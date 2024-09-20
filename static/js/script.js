document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('researchForm');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const emailExportElement = document.getElementById('emailExport');
    const emailForm = document.getElementById('emailForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const companyName = document.getElementById('companyName').value;
        const companyWebsite = document.getElementById('companyWebsite').value;

        // Show loading message and spinner
        loadingElement.style.display = 'block';
        loadingElement.innerHTML = '<p>Running Research Analysis</p><div class="spinner"></div>';
        resultsElement.innerHTML = '';
        emailExportElement.style.display = 'none';

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
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Parse the JSON data
            let jsonData;
            try {
                jsonData = JSON.parse(data);
            } catch (error) {
                throw new Error('Failed to parse JSON response');
            }

            // Define the desired order of sections
            const sectionOrder = [
                "Company Name",
                "Company Overview",
                "Recent News",
                "Competitors",
                "Investment Analysis"
            ];

            // Display results in HTML format with specified order
            let analysisHtml = '<h2>Research Results:</h2>';
            sectionOrder.forEach(section => {
                if (jsonData.hasOwnProperty(section)) {
                    analysisHtml += `<h3>${section}:</h3><p>${jsonData[section]}</p>`;
                }
            });

            // Add any additional sections not specified in the order
            for (const [key, value] of Object.entries(jsonData)) {
                if (!sectionOrder.includes(key)) {
                    analysisHtml += `<h3>${key}:</h3><p>${value}</p>`;
                }
            }

            resultsElement.innerHTML = analysisHtml;
            emailExportElement.style.display = 'block';
        })
        .catch(error => {
            // Hide loading message and spinner
            loadingElement.style.display = 'none';

            // Display detailed error message
            resultsElement.innerHTML = `<h2>Error:</h2><p>${error.message}</p>`;
            console.error('Error:', error);
        });
    });

    emailForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('emailInput').value;
        const researchData = resultsElement.innerHTML;

        fetch('/export_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'email': email,
                'research_data': researchData
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to send email export request. Please try again.');
        });
    });
});
