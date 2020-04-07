import pandas as pd


df = pd.read_csv('COVIDSummaryData.csv')
df = df[:-1]
df['Case Count'] =  df['Case Count'].astype(int)
df['Death Count'] =  df['Death Count'].astype(int)

df['Onset Date'] =pd.to_datetime(df['Onset Date'])
death_sum = df['Death Count'].groupby(df['Onset Date']).sum()

print(death_sum.sum())