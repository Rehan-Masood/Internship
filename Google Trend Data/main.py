import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():
    print("--- 1. Analyzing Tesla Trends ---")
    df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
    df_tesla['MONTH'] = pd.to_datetime(df_tesla['MONTH'])
    
    print(f"Tesla Data Range: {df_tesla['MONTH'].min()} to {df_tesla['MONTH'].max()}\n")

    print("--- 2. Analyzing Unemployment Data ---")
    df_ue_19 = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
    df_ue_19['MONTH'] = pd.to_datetime(df_ue_19['MONTH'])
    print(f"Pre-COVID Data Shape: {df_ue_19.shape}\n")

    print("--- 3. Resampling Bitcoin Data ---")
    df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
    df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')

    df_btc_search['MONTH'] = pd.to_datetime(df_btc_search['MONTH'])
    df_btc_price['DATE'] = pd.to_datetime(df_btc_price['DATE'])

    df_btc_monthly_price = df_btc_price.resample('ME', on='DATE').mean()
    
    df_btc_monthly_price.reset_index(inplace=True)
    
    print("Sample of Resampled Monthly Bitcoin Price:")
    print(df_btc_monthly_price.head(3))
    print("\n")

    print("Generating Tesla Trend Chart...")
    
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax1 = plt.subplots(figsize=(14, 8), dpi=120)
    ax2 = ax1.twinx()

    ax1.set_xlim([df_tesla['MONTH'].min(), df_tesla['MONTH'].max()])
    ax1.xaxis.set_major_locator(years)
    ax1.xaxis.set_major_formatter(years_fmt)
    ax1.xaxis.set_minor_locator(months)

    ax1.plot(df_tesla['MONTH'], df_tesla['TSLA_USD_CLOSE'], color='#E50914', linewidth=3, label='Tesla Stock Price')
    ax2.plot(df_tesla['MONTH'], df_tesla['TSLA_WEB_SEARCH'], color='skyblue', linewidth=3, label='Search Popularity')

    ax1.set_title('Tesla Web Search Popularity vs Stock Price', fontsize=16)
    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Tesla Stock Price ($ USD)', color='#E50914', fontsize=14)
    ax2.set_ylabel('Google Search Trend Index', color='skyblue', fontsize=14)

    print("Displaying chart... Close window to end program.")
    plt.show()

if __name__ == '__main__':
    main()