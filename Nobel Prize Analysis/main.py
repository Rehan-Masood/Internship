import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def main():
    print("--- 1. Loading Nobel Prize Dataset ---")
    df = pd.read_csv('nobel_prize_data.csv')
    print(f"Dataset Shape: {df.shape}")
    print(df.head(3))
    print("\n")

    print("--- 2. Data Cleaning & Age Calculation ---")
    
    print(f"Duplicate entries: {df.duplicated().sum()}")
    
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df['winning_age'] = df['year'] - df['birth_date'].dt.year

    youngest = df.loc[df['winning_age'].idxmin()]
    oldest = df.loc[df['winning_age'].idxmax()]

    print(f"Youngest Laureate: {youngest['full_name']} ({int(youngest['winning_age'])} years old in {youngest['year']})")
    print(f"Oldest Laureate: {oldest['full_name']} ({int(oldest['winning_age'])} years old in {oldest['year']})\n")

    print("--- 3. Visualizing Gender Ratio Over Time ---")
    
    gender_counts = df['sex'].value_counts()
    print(f"Gender Breakdown:\n{gender_counts}\n")

    df['decade'] = (df['year'] // 10) * 10
    
    plt.figure(figsize=(12, 6), dpi=120)
    sns.countplot(
        data=df,
        x='decade',
        hue='sex',
        palette={'Male': '#1f77b4', 'Female': '#e377c2'}
    )
    plt.title('Nobel Prize Winners by Gender Across Decades', fontsize=14)
    plt.xlabel('Decade', fontsize=12)
    plt.ylabel('Number of Laureates', fontsize=12)
    plt.legend(title='Gender')
    
    print("Displaying Gender Ratio Chart... Close plot window to continue.")
    plt.show()

    print("--- 4. Visualizing Top Country Rankings with Plotly ---")
    
    top_countries = df['birth_country_current'].value_counts().head(20).reset_index()
    top_countries.columns = ['country', 'count']

    fig_bar = px.bar(
        top_countries,
        x='count',
        y='country',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        title='Top 20 Nobel Prize Winning Countries (Birth Country)',
        labels={'count': 'Number of Prizes', 'country': 'Country'}
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig_bar.show()

    country_df = df.groupby(['birth_country_current', 'ISO'], as_index=False).agg({'prize': 'count'})
    
    fig_map = px.choropleth(
        country_df,
        locations='ISO',
        color='prize',
        hover_name='birth_country_current',
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Global Distribution of Nobel Laureates by Birth Country'
    )
    fig_map.show()

    print("--- 5. Visualizing Age Distribution per Category ---")
    
    plt.figure(figsize=(12, 6), dpi=120)
    sns.boxplot(
        data=df,
        x='category',
        y='winning_age',
        palette='Set2'
    )
    sns.stripplot(
        data=df,
        x='category',
        y='winning_age',
        color='black',
        alpha=0.3,
        jitter=0.2
    )
    plt.title('Age Distribution of Nobel Laureates by Category', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Age at Prize Award', fontsize=12)
    
    print("Displaying Category Age Distribution... Close window to end program.")
    plt.show()

if __name__ == '__main__':
    main()