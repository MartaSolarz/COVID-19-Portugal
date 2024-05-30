import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)

df = df[df['new_cases'] > 0]

sns.set_style("whitegrid")

plt.figure(figsize=(10, 6))
plt.plot(df.index, df['new_cases'], label='Portugal', color='red', alpha=0.7)

max_value = df['new_cases'].max()
max_date = df['new_cases'].idxmax()
plt.text(max_date, max_value, f'   Max: {max_value:,}\n   Date: {max_date.strftime("%d.%m.%Y")}', ha='left', va='center')

plt.xlabel('Date', fontsize=12)
plt.ylabel('New cases', fontsize=12)
plt.title('New COVID-19 cases in Portugal', fontsize=15, fontweight='bold')
plt.yticks([0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000], ['0', '50k', '100k', '150k', '200k', '250k', '300k', '350k', '400k', '450k'])
plt.grid(True, linestyle='--', color='grey', linewidth=0.5)

plt.savefig('../plots/2_new_cases_state.png')
