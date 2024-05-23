# This script creates a gif that shows the comparison between
# the number of new cases and the number of new deaths due to COVID-19 in Portugal.
# The data is resampled monthly and summed.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df.resample('M').sum()

def update(frame, ax, ax2, df):
    ax.clear()
    ax2.clear()

    ax.plot(df.index[:frame], df['new_cases'][:frame], color='red', label='New cases')
    ax.set_ylim(-10000, 2000000)
    ax.set_yticks([0, 500000, 1000000, 1500000, 2000000])
    ax.set_yticklabels(['0M', '0.5M', '1M', '1.5M', '2M'])
    ax.set_ylabel('Number of new cases')
    ax.grid(True, linestyle='--', color='red', alpha=0.3)
    ax.legend(loc='upper left')

    ax2.plot(df.index[:frame], df['new_deaths'][:frame], color='black', label='Deaths')
    ax2.set_ylim(-100, 7000)
    ax2.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
    ax2.set_yticklabels(['0', '1k', '2k', '3k', '4k', '5k', '6k', '7k'])
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.set_ylabel('Number of deaths', rotation=270, labelpad=25)
    ax2.grid(True, linestyle='--', color='black', alpha=0.3)
    ax2.legend(loc='upper right')

    case_pos = df['new_cases'][frame]
    ax.text(df.index[frame], case_pos, f'{case_pos:.0f}',
            ha='center', va='bottom', fontsize=8, color='red')

    death_pos = df['new_deaths'][frame] + 100
    ax2.text(df.index[frame], death_pos, f'{df["new_deaths"][frame]:.0f}',
             ha='center', va='top', fontsize=8, color='black')

    ax.set_title('Comparison of new cases and deaths due to COVID-19 in Portugal', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.xlim(df.index[0], df.index[-1])
    plt.text(0.51, 0.9, df.index[frame].strftime('%m.%Y'), transform=ax.transAxes,
             ha='center', fontsize=15)
    plt.tight_layout()


fig, ax = plt.subplots(figsize=(10, 6))

ax2 = ax.twinx()

anim = FuncAnimation(fig, update, fargs=(ax, ax2, df), frames=len(df), repeat=False)

anim.save('../plots/3_deaths_vs_cases.gif', dpi=150, writer='imagemagick', fps=2)
