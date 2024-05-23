import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/poland.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df_monthly = df.resample('M').max()

df_vaccinations = df_monthly[
    ['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred']]
df_vaccinations = df_vaccinations[:-7]  # Remove last 7 rows to avoid showing incomplete data
def update(frame):
    ax.clear()

    vaccination_data = {
        'At least one dose': df_vaccinations.iloc[frame]['people_vaccinated_per_hundred'],
        'Fully vaccinated': df_vaccinations.iloc[frame]['people_fully_vaccinated_per_hundred'],
        'Boosters administered': df_vaccinations.iloc[frame]['total_boosters_per_hundred']
    }
    bars = ax.bar(vaccination_data.keys(), vaccination_data.values(), color=['blue', 'green', 'red'])
    ax.set_ylim(0, 105)
    ax.set_title(f'Progress on vaccination against COVID-19 in Poland - {df_vaccinations.index[frame].strftime("%m.%Y")}', fontweight='bold')
    ax.set_ylabel('Number of people per hundred')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='black')

    for bar, value in zip(bars, vaccination_data.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1, f'{value:.2f}', ha='center', va='bottom')


fig, ax = plt.subplots()

ani = FuncAnimation(fig, update, frames=len(df_vaccinations), repeat=False)

ani.save('../plots/7_vaccinations_pl_animation.gif', writer='imagemagick', fps=3, dpi=150)