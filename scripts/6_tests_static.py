import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df_monthly = df.resample('M').agg({
    'total_tests': 'max',
    'new_tests': 'sum',
    'positive_rate': 'mean'
})

df_monthly = df_monthly[:22]

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Tests', color='black')
ax1.plot(df_monthly.index, df_monthly['total_tests'], label='Number of total tests performed', color=color)
ax1.plot(df_monthly.index, df_monthly['new_tests'], label='Number of newly performed tests', color='tab:green')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_yticks([0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000, 20000000])
ax1.set_yticklabels(['0M', '2M', '4M', '6M', '8M', '10M', '12M', '14M', '16M', '18M', '20M'])
ax1.grid(True, linestyle='--', color='black', alpha=0.3)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_ylabel('Positive Rate (%)', color=color, rotation=270, labelpad=25)
ax2.plot(df_monthly.index, df_monthly['positive_rate'], label='Positive Rate', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.grid(True, linestyle='--', color=color, alpha=0.3)

fig.legend(loc='upper left', bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
fig.suptitle('COVID-19 Testing Trends in Portugal', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig('../plots/6_tests.png', dpi=200)