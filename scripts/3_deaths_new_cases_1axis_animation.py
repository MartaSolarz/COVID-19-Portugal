import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df.resample('M').sum()

df['death_rate'] = (df['new_deaths'] / df['new_cases']) * 100
df['death_rate'] = df['death_rate'].fillna(0)

def update(frame, ax, df):
    ax.clear()

    ax.plot(df.index[:frame], df['new_cases'][:frame], color='red', label='New cases')
    ax.set_ylim(-100000, 2000000)
    ax.set_yticks([0, 500000, 1000000, 1500000, 2000000])
    ax.set_yticklabels(['0M', '0.5M', '1M', '1.5M', '2M'])
    plt.ylabel('Cases')
    ax.grid(True, linestyle='--', color='grey', alpha=0.3)

    ax.plot(df.index[:frame], df['new_deaths'][:frame], color='black', label='Deaths')

    plt.legend(loc='upper left')

    case_pos = df['new_cases'][frame]
    ax.text(df.index[frame], case_pos, f'{case_pos:.0f}',
            ha='center', va='bottom', fontsize=8, color='red')

    death_pos = df['new_deaths'][frame]
    ax.text(df.index[frame], death_pos, f'{df["new_deaths"][frame]:.0f}',
             ha='center', va='top', fontsize=8, color='black')

    ax.fill_between(df.index[:frame], df['new_cases'][:frame], color='red', alpha=0.1)
    ax.fill_between(df.index[:frame], df['new_deaths'][:frame], color='black', alpha=0.1)

    death_rate = df['death_rate'][frame]
    ax.text(0.8, 0.93, f'{death_rate:.2f}% death rate', transform=ax.transAxes,
            ha='center', va='top', fontsize=8, color='blue', bbox=dict(facecolor='white', alpha=0.5))

    ax.set_title('Comparison of new cases and deaths due to COVID-19 in Portugal', fontsize=14, fontweight='bold')
    plt.xlim(df.index[0], df.index[-1])
    plt.text(0.51, 0.9, df.index[frame].strftime('%m.%Y'), transform=ax.transAxes,
             ha='center', fontsize=15)


fig, ax = plt.subplots(figsize=(10, 6))

anim = FuncAnimation(fig, update, fargs=(ax, df), frames=len(df), repeat=False)

anim.save('../plots/3_deaths_vs_cases_one_axis.gif', dpi=150, writer='imagemagick', fps=3)
