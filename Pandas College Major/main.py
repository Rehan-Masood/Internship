import pandas as pd

def main():
    print("--- 1. Loading Dataset ---")
    df = pd.read_csv('salaries_by_college_major.csv')
    print(f"Dataset Shape: {df.shape}")
    print(df.head())
    print("\n")

    print("--- 2. Cleaning Missing Data ---")
    clean_df = df.dropna()
    print(f"Cleaned Shape: {clean_df.shape}\n")

    print("--- 3. Salary Extremes ---")
    
    max_start_id = clean_df['Starting Median Salary'].idxmax()
    print(f"Highest Starting Salary: {clean_df.loc[max_start_id, 'Undergraduate Major']} "
          f"(${clean_df.loc[max_start_id, 'Starting Median Salary']:,.2f})")

    max_mid_id = clean_df['Mid-Career Median Salary'].idxmax()
    print(f"Highest Mid-Career Salary: {clean_df.loc[max_mid_id, 'Undergraduate Major']} "
          f"(${clean_df.loc[max_mid_id, 'Mid-Career Median Salary']:,.2f})")

    min_start_id = clean_df['Starting Median Salary'].idxmin()
    print(f"Lowest Starting Salary: {clean_df.loc[min_start_id, 'Undergraduate Major']} "
          f"(${clean_df.loc[min_start_id, 'Starting Median Salary']:,.2f})\n")

    print("--- 4. Financial Risk Analysis (90th - 10th Percentile Spread) ---")
    spread = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
    
    if 'Spread' not in clean_df.columns:
        clean_df.insert(1, 'Spread', spread)

    low_risk = clean_df.sort_values('Spread')
    print("\nMajors with Lowest Financial Risk:")
    print(low_risk[['Undergraduate Major', 'Spread']].head())

    high_risk = clean_df.sort_values('Spread', ascending=False)
    print("\nMajors with Highest Financial Risk / Spread:")
    print(high_risk[['Undergraduate Major', 'Spread']].head())
    print("\n")

    print("--- 5. Average Salary Metrics by Group ---")
    pd.options.display.float_format = '{:,.2f}'.format
    
    if 'Group' in clean_df.columns:
        group_stats = clean_df.groupby('Group').mean(numeric_only=True)
        print(group_stats[['Starting Median Salary', 'Mid-Career Median Salary', 'Spread']])
    else:
        print("Note: 'Group' column not present in standard dataset.")

if __name__ == '__main__':
    main()