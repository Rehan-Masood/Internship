import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
    
    print("--- First 5 Rows of Data ---")
    print(df.head())
    
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    pivoted_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
    
    pivoted_df.fillna(0, inplace=True)
    
    print("\n--- Reshaped Data Sample (Pivoted) ---")
    print(pivoted_df.head())

    roll_df = pivoted_df.rolling(window=6).mean()

    plt.figure(figsize=(16, 10))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Number of Posts', fontsize=14)
    plt.title('Popularity of Programming Languages on Stack Overflow', fontsize=16)
    
    plt.ylim(0, 35000)
    
    languages_to_plot = ['python', 'java', 'javascript', 'c++', 'r']
    for lang in languages_to_plot:
        if lang in roll_df.columns:
            plt.plot(roll_df.index, roll_df[lang], linewidth=3, label=lang.capitalize())
            
    plt.legend(fontsize=16)
    
    print("\nDisplaying trend chart... Close the chart window to end the script.")
    plt.show()

if __name__ == '__main__':
    main()