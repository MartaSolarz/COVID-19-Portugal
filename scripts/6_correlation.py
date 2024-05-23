import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv')

df = df.dropna(subset=['positive_rate', 'total_tests'])


sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.scatter(df['total_tests'], df['positive_rate'], alpha=0.3, color='blue')
plt.title('Correlation between the total number of tests performed\nand the percentage of positive results in Portugal', fontsize=15, fontweight='bold')

sns.regplot(x='total_tests', y='positive_rate', data=df, scatter=False, color='red')

plt.xlabel('Total Tests Performed')
plt.ylabel('Positive Rate (%)')
plt.xticks([0, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000, 35000000, 40000000, 45000000], ['0', '5M', '10M', '15M', '20M', '25M', '30M', '35M', '40M', '45M'])

plt.grid(True, linestyle='--', color='grey', linewidth=0.5)

plt.tight_layout()

plt.savefig('../plots/6_tests_correlation.png', dpi=200)
