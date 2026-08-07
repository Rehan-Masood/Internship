import pandas as pd
import plotly.express as px

def main():
    df_apps = pd.read_csv('apps.csv')
    
    print("--- 1. Initial Data Inspection ---")
    print(f"Dataset Dimensions: {df_apps.shape}")
    print(df_apps.sample(3))
    print("\n")

    df_clean = df_apps.drop(columns=['Last_Updated', 'Android_Ver']).dropna().copy()
    print(f"Dimensions after dropping NaNs: {df_clean.shape}\n")

    print("--- 2. Cleaning Numerical Formatting Errors ---")
    
    installs_clean = df_clean['Installs'].astype(str).str.replace(',', '', regex=False)
    installs_clean = installs_clean.str.replace('+', '', regex=False)
    df_clean['Installs'] = pd.to_numeric(installs_clean)

    price_clean = df_clean['Price'].astype(str).str.replace('$', '', regex=False)
    df_clean['Price'] = pd.to_numeric(price_clean)
    
    print("Top Most Expensive Paid Apps:")
    print(df_clean.sort_values('Price', ascending=False)[['App', 'Price']].head(3))
    print("\n")

    top_categories = df_clean['Category'].value_counts()
    category_summary = df_clean.groupby('Category').agg({'App': 'count', 'Installs': 'sum'})

    print("Generating Interactive Plotly Charts...")
    
    fig_bar = px.bar(
        x=top_categories.index, 
        y=top_categories.values,
        title='Number of Apps Per Category on the Google Play Store',
        labels={'x': 'Category', 'y': 'Number of Apps'}
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    fig_bar.show()

    fig_bubble = px.scatter(
        category_summary,
        x='App',
        y='Installs',
        size='App',       
        hover_name=category_summary.index,
        color='Installs', 
        title='Category Popularity: App Volume vs. Total Downloads',
        labels={'App': 'Number of Apps (Volume)', 'Installs': 'Total Installations'}
    )
    fig_bubble.show()

if __name__ == '__main__':
    main()