# CustomerChurn Intelligence Pro

A small Streamlit-based demo app that generates synthetic customer data, trains a Random Forest classifier to predict churn, and provides an interactive dashboard for EDA, live prediction, and model diagnostics.

## Demo Video
<video src="https://github.com/user-attachments/assets/c20d5485-7756-4d58-ad66-9a13eb22ff69" controls width="600"></video>

## Features
- Synthetic dataset generation (tenure, monthly charges, support tickets, contract/payment types)
- Exploratory Data Analysis with interactive Plotly charts
- Live churn risk predictor (interactive inputs + probability score)
- Model performance view: accuracy, feature importances, confusion matrix

## Requirements
- Python 3.8+
- Packages: `streamlit`, `pandas`, `numpy`, `scikit-learn`, `plotly`

You can install dependencies into a virtual environment:

```bash
python -m venv .venv
# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1
# or (CMD)
.\.venv\Scripts\activate
# then
pip install streamlit pandas numpy scikit-learn plotly
```

Optionally, create a `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Quick Start

Run the Streamlit app from the project root:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Project Layout
- `app.py` — Streamlit application (data generation, model training, dashboard)

## Notes
- The app uses a synthetic dataset generated at runtime for demo and learning purposes.
- Model hyperparameters are basic and intended for demonstration, not production use.

If you'd like, I can also generate a `requirements.txt`, add example screenshots, or expand the README with deployment instructions.
