import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df_pl = pd.read_csv('../data/poland.csv', index_col='date', parse_dates=True)

df = df[df['total_cases'] > 0]
df_pl = df_pl[df_pl['total_cases'] > 0]

sns.set_style("whitegrid")

plt.figure(figsize=(10, 6))

plt.plot(df.index, df['total_cases'], label='Portugal', color='red')
plt.plot(df_pl.index, df_pl['total_cases'], label='Poland', color='grey', alpha=0.4)

plt.legend()

plt.xlabel('Date', fontsize=12)
plt.ylabel('Total cases', fontsize=12)
plt.ylim(-100000, 7500000)
plt.yticks([0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000], ['0M', '1M', '2M', '3M', '4M', '5M', '6M', '7M'])

plt.title('Comparison of the total number of COVID-19 cases\nthroughout the pandemic in Portugal and Poland', fontsize=15, fontweight='bold')

plt.grid(True, linestyle='--')

plt.fill_between(df.index, df['total_cases'], color='red', alpha=0.1)
plt.fill_between(df_pl.index, df_pl['total_cases'], color='grey', alpha=0.15)

plt.savefig('../plots/1_total_cases_static.png')
