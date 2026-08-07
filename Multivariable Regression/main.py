import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def main():
    print("--- 1. Loading Boston Housing Dataset ---")
    df = pd.read_csv('boston.csv', index_col=0) # Unnamed index column
    print(f"Dataset Shape: {df.shape}")
    print(f"Missing Values: {df.isna().sum().sum()}")
    print(f"Duplicate Rows: {df.duplicated().sum()}\n")

    print(df.describe()[['RM', 'LSTAT', 'NOX', 'PRICE']])
    print("\n")

    print("--- 2. Visualizing Relationships ---")
    plt.figure(figsize=(10, 6), dpi=120)
    sns.regplot(
        data=df,
        x='RM',
        y='PRICE',
        scatter_kws={'alpha': 0.5},
        line_kws={'color': 'red'}
    )
    plt.title('Number of Rooms (RM) vs. House Price (PRICE)', fontsize=14)
    plt.xlabel('Average Rooms per Dwelling', fontsize=12)
    plt.ylabel('Price in $1,000s', fontsize=12)
    
    print("Displaying Rooms vs Price chart... Close plot window to proceed.")
    plt.show()

    print("--- 3. Fitting Baseline Multivariable Regression ---")
    
    X = df.drop(columns=['PRICE'])
    y = df['PRICE']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=10
    )

    regr = LinearRegression()
    regr.fit(X_train, y_train)

    r2_train = regr.score(X_train, y_train)
    r2_test = regr.score(X_test, y_test)

    print(f"Base Model Training R²: {r2_train:.4f}")
    print(f"Base Model Testing  R²: {r2_test:.4f}\n")

    print("--- 4. Fitting Log-Transformed Target Model ---")
    
    y_log = np.log(df['PRICE'])

    X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(
        X, y_log, test_size=0.2, random_state=10
    )

    log_regr = LinearRegression()
    log_regr.fit(X_train_log, y_train_log)

    log_r2_train = log_regr.score(X_train_log, y_train_log)
    log_r2_test = log_regr.score(X_test_log, y_test_log)

    print(f"Log Model Training R²: {log_r2_train:.4f}")
    print(f"Log Model Testing  R²: {log_r2_test:.4f}\n")

    print("--- 5. Property Valuation Example ---")
    
    sample_property = X.mean().to_frame().T
    sample_property['RM'] = 6.5
    sample_property['PTRATIO'] = 15.0
    sample_property['LSTAT'] = 5.0
    sample_property['CHAS'] = 1.0

    log_price_pred = log_regr.predict(sample_property)[0]
    dollar_est = np.exp(log_price_pred) * 1000 

    print(f"Predicted Log Price:        {log_price_pred:.4f}")
    print(f"Estimated Property Valuation: ${dollar_est:,.2f}")

if __name__ == '__main__':
    main()