# Multivariable Regression and Valuation Model

A small Python project that explores the Boston Housing dataset, visualizes the relationship between average rooms and house price, and fits two linear regression models for property valuation:

- a baseline multivariable linear regression model
- a log-transformed target regression model for improved fit on skewed prices

The script also produces a sample valuation estimate for a hypothetical property.

## Demo Video
<video src="https://github.com/user-attachments/assets/f88f7075-f3b7-49b9-9a0e-bedd2037289c" controls width="600"></video>

## Project Files

- `main.py` - main script that loads the data, trains the models, and prints the results
- `boston.csv` - Boston Housing dataset used by the script
- `requirements.txt` - Python dependencies required to run the project
- `Multivariable_Regression_and_Valuation_Model_(complete).ipynb` - notebook version of the analysis

## Features

- loads and inspects the Boston Housing dataset
- checks basic data quality metrics such as missing values and duplicates
- visualizes the relationship between number of rooms (`RM`) and house price (`PRICE`)
- trains a multivariable linear regression model
- trains a second model using a log-transformed target
- estimates a sample property valuation from the trained model

## Requirements

- Python 3.9 or later is recommended
- Packages listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## How to Run

From the project folder, run:

```bash
python main.py
```

The script will:

1. load `boston.csv`
2. print dataset summary statistics
3. display a scatter/regression plot for `RM` vs `PRICE`
4. train both regression models
5. print training and testing R-squared values
6. output an example property valuation

## Notes

- The dataset price values are scaled in thousands of dollars, so the final valuation is converted back to dollars in the script.
- The plot window must be closed before the script continues to the modeling steps.

## Repository Purpose

This project is useful as a compact regression workflow example for exploratory data analysis, model fitting, and basic valuation estimation using scikit-learn.
