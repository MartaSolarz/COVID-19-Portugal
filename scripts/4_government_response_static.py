import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df.resample('M').agg({
    'new_cases': 'sum',
    'new_deaths': 'sum',
    'stringency_index': 'mean'
})

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df.index, df['new_cases'], label='New Cases', color='blue')

ax.set_xlabel('Date')
ax.set_ylabel('Number of Cases')
ax.set_title('COVID-19 Government Response in Portugal', fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', color='blue', alpha=0.3)
ax.set_ylim(-50000, 1700000)
ax.set_yticks([0, 500000, 1000000, 1500000])
ax.set_yticklabels(['0M', '0.5M', '1M', '1.5M'])
ax.fill_between(df.index, df['new_cases'], color='blue', alpha=0.1)

ax2 = ax.twinx()
ax2.plot(df.index, df['stringency_index'], label='Stringency Index', color='red')
ax2.set_ylabel('Stringency Index', rotation=270, labelpad=20)
ax2.set_ylim(-3, 100)
ax2.grid(True, linestyle='--', color='red', alpha=0.3)
ax2.fill_between(df.index, df['stringency_index'], color='red', alpha=0.1)

fig.legend(loc='upper left', bbox_to_anchor=(0.75, 1), bbox_transform=ax.transAxes)
plt.tight_layout()

plt.savefig('../plots/4_government_response_static.png', dpi=200)
