import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('../data/portugal.csv', parse_dates=['date'])
df_pl = pd.read_csv('../data/poland.csv', parse_dates=['date'])

sns.set(style='whitegrid')
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['reproduction_rate'], linestyle='-', color='red', label='Portugal')
plt.plot(df_pl['date'], df_pl['reproduction_rate'], linestyle='-', color='grey', label='Poland', alpha=0.4)

plt.title('Comparison of COVID-19 Reproduction Rate in Portugal and Poland', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('Date', fontsize=12)
plt.ylabel('Reproduction rate (Rt)', fontsize=12)
plt.grid(True, linestyle='--', color='grey', linewidth=0.5)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.ylim(0, 3)
plt.legend()
plt.tight_layout()

plt.savefig('../plots/5_reproduction_rate_static.png', dpi=200)
