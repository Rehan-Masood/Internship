from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PROJECTS = [
    {
        "id": 1,
        "title": "Text to Morse Code Converter",
        "category": "Python CLI Utility",
        "description": "An interactive command-line application converting plain text to international Morse code with custom input parsing.",
        "tags": ["Python", "CLI", "Data Structures"],
        "github_url": "https://github.com/Rehan-Masood/Internship/tree/main/Morse%20Code%20Converter",
        "badge": "CLI"
    },
    {
        "id": 2,
        "title": "Google Play Store Analytics",
        "category": "Data Science & Plotly",
        "description": "Interactive data dashboard examining app downloads, pricing tiers, and category performance across 10,000+ apps.",
        "tags": ["Pandas", "Plotly", "Data Analysis"],
        "github_url": "https://github.com/Rehan-Masood/Internship/tree/main/Google%20Playstore%20Analysis",
        "badge": "Interactive"
    },
    {
        "id": 3,
        "title": "Boston House Price Predictor",
        "category": "Machine Learning",
        "description": "Multivariable linear regression model utilizing log transformations to accurately forecast property valuations.",
        "tags": ["Scikit-Learn", "Seaborn", "Regression"],
        "github_url": "https://github.com",
        "badge": "ML Model"
    },
    {
        "id": 4,
        "title": "Handwashing Mortality t-Test",
        "category": "Medical Statistics",
        "description": "Statistical hypothesis testing using Welch's t-test to validate Dr. Semmelweis's 19th-century medical discovery.",
        "tags": ["SciPy", "Matplotlib", "Statistics"],
        "github_url": "https://github.com",
        "badge": "Analytics"
    }
]

@app.route('/')
def home():
    stats = {
        "projects_completed": len(PROJECTS),
        "code_commits": "500+",
        "technologies": 12
    }
    return render_template('index.html', projects=PROJECTS, stats=stats)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print(f"\n📥 NEW CONTACT MESSAGE FROM {name.upper()} ({email}):")
        print(f"Message: {message}\n")

        return render_template('contact_success.html', name=name)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)