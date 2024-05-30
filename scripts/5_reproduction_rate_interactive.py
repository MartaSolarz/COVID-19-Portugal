import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/portugal.csv', parse_dates=['date'])
df_pl = pd.read_csv('../data/poland.csv', parse_dates=['date'])

# cut off empty data
df = df[df['date'] < '2023-01-05']
df_pl = df_pl[df_pl['date'] < '2023-01-05']

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['date'], y=df['reproduction_rate'], mode='lines',
                         name='Portugal', line=dict(color='red')))

fig.add_trace(go.Scatter(x=df_pl['date'], y=df_pl['reproduction_rate'], mode='lines',
                         name='Poland', line=dict(color='grey'), opacity=0.4))

fig.update_layout(
    title='Comparison of COVID-19 Reproduction Rate in Portugal and Poland',
    title_font=dict(size=20, family='Arial', color='black'),
    xaxis_title='Date',
    yaxis_title='Reproduction rate (Rt)',
    yaxis=dict(range=[0, 3]),
    legend_title='Country',
    template='plotly_white',
    hovermode='x'
)

fig.update_traces(
    hoverinfo='name+y+x'
)

fig.update_xaxes(
    tickformat="%d.%m.%Y",
    ticklabelmode="period"
)


fig.write_html('../plots/5_reproduction_rate_interactive.html')
