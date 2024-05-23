import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df[:'2022-02-28']

df = df[df['new_deaths'] > 0]

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['icu_patients'], label='ICU Patients', color='red')
plt.plot(df.index, df['hosp_patients'], label='Hospital Patients', color='blue')
plt.scatter(df.index, df['new_deaths'], label='New Weekly Deaths', color='black', marker='x', s=15)

plt.title('ICU, Hospital Patients and Weekly Deaths due to COVID-19 in Portugal', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('Date')
plt.ylabel('Number of Patients')
plt.legend()
plt.grid(True, linestyle='--', color='grey', linewidth=0.5)

plt.tight_layout()

plt.savefig('../plots/8_hospitals_static.png', dpi=200)