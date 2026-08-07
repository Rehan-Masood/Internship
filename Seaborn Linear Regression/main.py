import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

def main():
    print("--- 1. Loading Movie Budget Dataset ---")
    data = pd.read_csv('cost_revenue_dirty.csv')
    print(f"Initial Shape: {data.shape}")
    print(data.head(3))
    print("\n")

    print("--- 2. Cleaning Currency and Date Formats ---")
    
    chars_to_remove = [',', '$']
    columns_to_clean = ['USD_Production_Budget', 'USD_Worldwide_Gross', 'USD_Domestic_Gross']

    for col in columns_to_clean:
        for char in chars_to_remove:
            data[col] = data[col].astype(str).str.replace(char, '', regex=False)
        data[col] = pd.to_numeric(data[col])

    data['Release_Date'] = pd.to_datetime(data['Release_Date'])

    old_films = data[data['Release_Date'] < '1970-01-01']
    new_films = data[data['Release_Date'] >= '1970-01-01']

    clean_data = data[data['USD_Worldwide_Gross'] != 0].copy()
    print(f"Cleaned Dataset Shape: {clean_data.shape}\n")

    print("--- 3. Visualizing Budget vs. Revenue with Seaborn ---")
    plt.figure(figsize=(12, 6), dpi=120)
    
    ax = sns.regplot(
        data=new_films,
        x='USD_Production_Budget',
        y='USD_Worldwide_Gross',
        color='#2f4b7c',
        scatter_kws={'alpha': 0.4},
        line_kws={'color': '#ff7c43'}
    )

    ax.set(
        ylim=(0, 3000000000),
        xlim=(0, 4500000000),
        ylabel='Revenue in $ Billions',
        xlabel='Budget in $ Millions',
        title='Worldwide Box Office Revenue vs. Production Budget (1970 - Present)'
    )
    
    print("Displaying Seaborn Regression Plot... Close plot window to continue script execution.")
    plt.show()

    print("--- 4. Fitting Linear Regression Model ---")
    
    X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
    y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

    regression = LinearRegression()
    regression.fit(X, y)

    r_squared = regression.score(X, y)
    intercept = regression.intercept_[0]
    slope = regression.coef_[0][0]

    print(f"R-Squared Score (Model Fit): {r_squared:.4f}")
    print(f"Model Intercept (β0): {intercept:,.2f}")
    print(f"Model Slope / Coefficient (β1): {slope:.4f}")
    print(f"\nLinear Equation: Revenue = {intercept:,.0f} + {slope:.2f} * Budget")

    budget_test = 350000000  # $350 Million Budget
    revenue_pred = regression.predict([[budget_test]])[0][0]
    print(f"\nPredicted Worldwide Revenue for a $350M Budget Movie: ${revenue_pred:,.2f}")

if __name__ == '__main__':
    main()