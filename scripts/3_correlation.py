import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv')

df = df.dropna(subset=['new_deaths', 'new_cases'])

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.scatter(df['new_cases'], df['new_deaths'], alpha=0.3, color='blue')
plt.title('Correlation between the number of new COVID-19 cases and new deaths in Portugal', fontsize=15, fontweight='bold')

sns.regplot(x='new_cases', y='new_deaths', data=df, scatter=False, color='red')

plt.ylabel('New Deaths')
plt.xlabel('New Cases')
plt.xticks([0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000], ['0', '50k', '100k', '150k', '200k', '250k', '300k', '350k', '400k', '450k'])

plt.grid(True, linestyle='--', color='grey', linewidth=0.5)

plt.tight_layout()

plt.savefig('../plots/3_deaths_cases_correlation.png', dpi=200)
