import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df[:'2022-02-28']
df = df[df['new_deaths'] > 0]

df_pl = pd.read_csv('../data/poland.csv', index_col='date', parse_dates=True)
df_pl.fillna(0, inplace=True)

df_pl = df_pl[:'2022-02-28']
df_pl = df_pl[df_pl['new_deaths'] > 0]

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['hosp_patients'], label='Hospital Patients (PT)', color='blue')
plt.scatter(df.index, df['new_deaths'], label='New Weekly Deaths (PT)', color='black', marker='x', s=15)

plt.plot(df_pl.index, df_pl['hosp_patients'], label='Hospital Patients (PL)', color='blue', linestyle='-', alpha=0.4)
plt.scatter(df_pl.index, df_pl['new_deaths'], label='New Weekly Deaths (PL)', color='black', marker='x', s=15, alpha=0.4)

plt.title('Hospital Patients and Weekly Deaths due to COVID-19 in Portugal and Poland', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('Date')
plt.ylabel('Number of Patients')
plt.yticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000], ['0', '5k', '10k', '15k', '20k', '25k', '30k', '35k'])
plt.legend()
plt.grid(True, linestyle='--', color='grey', linewidth=0.5)

plt.tight_layout()

plt.savefig('../plots/8_hospitals_comparison_static.png', dpi=200)