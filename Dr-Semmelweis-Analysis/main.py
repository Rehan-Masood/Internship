import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
from scipy import stats

def main():
    print("--- 1. Annual Mortality Analysis by Clinic ---")
    df_annual = pd.read_csv('annual_deaths_by_clinic.csv')
    
    df_annual['pct_deaths'] = (df_annual['deaths'] / df_annual['births']) * 100
    
    clinic_1 = df_annual[df_annual['clinic'] == 'clinic 1']
    clinic_2 = df_annual[df_annual['clinic'] == 'clinic 2']

    print("Average Death Rate Clinic 1 (Medical Students):", f"{clinic_1['pct_deaths'].mean():.2f}%")
    print("Average Death Rate Clinic 2 (Midwives):", f"{clinic_2['pct_deaths'].mean():.2f}%\n")

    fig_annual = px.line(
        df_annual,
        x='year',
        y='pct_deaths',
        color='clinic',
        title='Annual Proportion of Deaths at Vienna General Hospital (1841-1846)',
        labels={'pct_deaths': 'Percentage of Maternal Deaths (%)', 'year': 'Year'}
    )
    fig_annual.show()

    print("--- 2. Monthly Mortality Analysis & Intervention ---")
    df_monthly = pd.read_csv('monthly_deaths.csv')
    df_monthly['date'] = pd.to_datetime(df_monthly['date'])
    df_monthly['pct_deaths'] = (df_monthly['deaths'] / df_monthly['births']) * 100

    handwashing_start = pd.to_datetime('1847-06-01')

    before_washing = df_monthly[df_monthly['date'] < handwashing_start]
    after_washing = df_monthly[df_monthly['date'] >= handwashing_start]

    mean_before = before_washing['pct_deaths'].mean()
    mean_after = after_washing['pct_deaths'].mean()

    print(f"Mean death rate BEFORE handwashing: {mean_before:.2f}%")
    print(f"Mean death rate AFTER handwashing:  {mean_after:.2f}%")
    print(f"Absolute reduction in mortality:    {mean_before - mean_after:.2f}%\n")

    print("Generating Monthly Mortality Line Plot with Intervention Marker...")
    
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots(figsize=(14, 7), dpi=120)
    
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)
    ax.set_xlim([df_monthly['date'].min(), df_monthly['date'].max()])

    ax.plot(before_washing['date'], before_washing['pct_deaths'], color='crimson', label='Before Handwashing', linewidth=2)
    ax.plot(after_washing['date'], after_washing['pct_deaths'], color='skyblue', label='After Handwashing', linewidth=3)
    
    ax.axvline(x=handwashing_start, color='black', linestyle='--', linewidth=1.5, label='Handwashing Enforced')

    ax.set_title('Monthly Maternal Mortality Rate Before & After Handwashing (1841–1849)', fontsize=15)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Percentage of Deaths (%)', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(color='grey', linestyle='--', linewidth=0.5, alpha=0.5)

    print("Displaying timeline plot... Close chart window to proceed to statistical testing.")
    plt.show()

    print("--- 3. Hypothesis Testing: Two-Sample Independent t-Test ---")
    
    t_stat, p_value = stats.ttest_ind(
        a=before_washing['pct_deaths'],
        b=after_washing['pct_deaths'],
        equal_var=False
    )

    print(f"t-Statistic: {t_stat:.4f}")
    print(f"p-Value:     {p_value:.10f}")

    if p_value < 0.01:
        print("\nConclusion: The difference is STATISTICALLY SIGNIFICANT at the 99% confidence level!")
        print("We reject the null hypothesis — handwashing directly reduced hospital mortality.")
    else:
        print("\nConclusion: Failed to reject the null hypothesis.")

if __name__ == '__main__':
    main()