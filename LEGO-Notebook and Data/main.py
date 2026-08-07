import pandas as pd
import matplotlib.pyplot as plt

def main():
    colors_df = pd.read_csv('colors.csv')
    sets_df = pd.read_csv('sets.csv')
    themes_df = pd.read_csv('themes.csv')
    
    print("--- 1. Exploring LEGO Colors ---")
    print(f"Total unique LEGO colors: {colors_df['name'].nunique()}")
    transparent_counts = colors_df.groupby('is_trans').count()
    print(f"Transparent vs Opaque counts:\n{transparent_counts['id']}\n")

    print("--- 2. Exploring LEGO Sets ---")
    print("Oldest LEGO sets released:")
    print(sets_df.sort_values('year').head(3)[['year', 'name']])
    
    top_parts = sets_df.sort_values('num_parts', ascending=False).iloc[0]
    print(f"\nSet with most parts: {top_parts['name']} ({top_parts['num_parts']} parts)\n")

    print("--- 3. Aggregation: Sets per Year ---")
    sets_by_year = sets_df.groupby('year').count()['set_num'][:-1] # Exclude incomplete current year data
    print(sets_by_year.tail())
    
    themes_by_year = sets_df.groupby('year').agg({'theme_id': pd.Series.nunique})[:-1]
    themes_by_year.rename(columns={'theme_id': 'nr_themes'}, inplace=True)

    print("\n--- 4. Merging Data: Themes and Sets ---")
    set_theme_counts = sets_df['theme_id'].value_counts()
    set_theme_counts = pd.DataFrame({'id': set_theme_counts.index, 'set_count': set_theme_counts.values})
    
    merged_df = pd.merge(set_theme_counts, themes_df, on='id')
    print("Top 5 most popular LEGO themes based on set count:")
    print(merged_df[['name', 'set_count']].head())

    fig, ax1 = plt.subplots(figsize=(16, 10))
    ax2 = ax1.twinx() # Share the x-axis

    ax1.plot(sets_by_year.index, sets_by_year.values, color='g', linewidth=3, label='Number of Sets')
    ax2.plot(themes_by_year.index, themes_by_year['nr_themes'], color='b', linewidth=3, label='Number of Themes')

    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Number of Sets', color='g', fontsize=14)
    ax2.set_ylabel('Number of Themes', color='b', fontsize=14)
    plt.title('LEGO Production Growth Trends (1949 - 2025)', fontsize=16)
    
    print("\nDisplaying trend chart... Close the chart window to complete execution.")
    plt.show()

if __name__ == '__main__':
    main()