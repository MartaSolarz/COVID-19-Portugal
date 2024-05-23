import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df.resample('M').sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax2 = ax.twinx()

ax.plot(df.index, df['new_cases'], color='red', label='New cases')
ax.set_ylim(-10000, 1700000)
ax.set_yticks([0, 500000, 1000000, 1500000])
ax.set_yticklabels(['0M', '0.5M', '1M', '1.5M'])
ax.set_ylabel('Number of new cases')
ax.grid(True, linestyle='--', color='red', alpha=0.3)
ax.legend(loc='upper left')

ax2.plot(df.index, df['new_deaths'], color='black', label='Deaths')
ax2.set_ylim(-100, 7000)
ax2.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
ax2.set_yticklabels(['0', '1k', '2k', '3k', '4k', '5k', '6k', '7k'])
ax2.set_ylabel('Number of deaths', rotation=270, labelpad=25)
ax2.grid(True, linestyle='--', color='black', alpha=0.3)
ax2.legend(loc='upper right')

ax.set_title('Comparison of new Cases and deaths due to COVID-19 in Portugal', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)

plt.xlim(df.index[0], df.index[-1])
plt.tight_layout()

max_cases = df['new_cases'].max()
max_deaths = df['new_deaths'].max()
max_cases_date = df['new_cases'].idxmax()
max_deaths_date = df['new_deaths'].idxmax()

ax.text(max_cases_date, max_cases + 30000, f'Max: {max_cases:,}\nDate: {max_cases_date.strftime("%m.%Y")}\n',
        ha='center', va='bottom', fontsize=8, color='red', backgroundcolor='white')
ax2.text(max_deaths_date, max_deaths + 100, f'Max: {max_deaths:,}\nDate: {max_deaths_date.strftime("%m.%Y")}', backgroundcolor='white',
         ha='center', va='bottom', fontsize=8, color='black')

plt.savefig('../plots/3_deaths_cases_static.png', dpi=200)
