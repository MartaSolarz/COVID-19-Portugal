import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import seaborn as sns


def update(frame, ax, df):
    ax.clear()

    ax.bar(['Portugal', 'Poland'], df.iloc[frame], color=['red', 'grey'], edgecolor='black')

    ax.set_ylabel('Number of cases')
    ax.set_title('Increase in the number of COVID-19 cases\nin Portugal and Poland\n', fontsize=14, fontweight='bold')

    plt.yticks([0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000],
               ['0M', '1M', '2M', '3M', '4M', '5M', '6M', '7M'])

    ax.grid(True, linestyle='--', axis='y', which='major', color='black', alpha=0.3)

    ax.text(0.5, -0.08, df.index[frame].strftime('%m-%Y'), transform=ax.transAxes, ha='center', fontsize=15)

    for i, value in enumerate(df.iloc[frame]):
        ax.text(i, value + 20000, value, ha='center', fontsize=10)


df_portugal = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)['new_cases']
df_poland = pd.read_csv('../data/poland.csv', index_col='date', parse_dates=True)['new_cases']

df_portugal = df_portugal.resample('M').sum()
df_poland = df_poland.resample('M').sum()

for i in range(1, len(df_portugal)):
    df_portugal.iloc[i] += df_portugal.iloc[i - 1]

for i in range(1, len(df_poland)):
    df_poland.iloc[i] += df_poland.iloc[i - 1]

df = pd.concat([df_portugal, df_poland], axis=1)
df.columns = ['Portugal', 'Poland']

sns.set_style('whitegrid')

fig, ax = plt.subplots(figsize=(6, 6))

anim = FuncAnimation(fig, update, fargs=(ax, df), frames=len(df), repeat=False)

anim.save('../plots/1_cases_growth.gif', dpi=150, writer='imagemagick', fps=4)
