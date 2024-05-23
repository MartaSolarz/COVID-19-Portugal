import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df_monthly = df.resample('M').max()
df_vaccinations = df_monthly[
    ['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred']]
df_vaccinations = df_vaccinations[:-7]


plt.figure(figsize=(10, 6))
plt.plot(df_vaccinations.index, df_vaccinations['people_vaccinated_per_hundred'], label='At least one dose', color='blue', marker='o')
plt.plot(df_vaccinations.index, df_vaccinations['people_fully_vaccinated_per_hundred'], label='Fully vaccinated', color='green', marker='o')
plt.plot(df_vaccinations.index, df_vaccinations['total_boosters_per_hundred'], label='Boosters administered', color='red', marker='o')

plt.title('COVID-19 Vaccination Progress in Portugal', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of people per hundred', fontsize=12)

plt.legend()
plt.grid(True, linestyle='--', color='grey', linewidth=0.5)
plt.ylim(-2, 110)

plt.tight_layout()

plt.savefig('../plots/7_vaccinations_static.png', dpi=200)
