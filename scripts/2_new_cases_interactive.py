import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/portugal.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

df = df[df['new_cases'] > 0]

fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df['new_cases'], mode='lines+markers',
                         name='New Cases', line=dict(color='red', width=1), marker=dict(size=5)))


max_value = df['new_cases'].max()
max_date = df['new_cases'].idxmax()
fig.add_annotation(x=max_date, y=max_value,
                   text=f'Max number of new cases<br>Date: {max_date.strftime("%d.%m.%Y")}')

fig.update_layout(
    title='New COVID-19 cases in Portugal',
    xaxis_title='Date',
    yaxis_title='New cases',
    yaxis=dict(tickmode='array',
               tickvals=[0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000],
               ticktext=['0', '50k', '100k', '150k', '200k', '250k', '300k', '350k', '400k', '450k']),
    template='plotly_white',
    hovermode='x'
)

fig.update_xaxes(
    tickformat="%d.%m.%Y",
    ticklabelmode="period"
)

fig.write_html('../plots/2_new_cases_state_interactive.html')
