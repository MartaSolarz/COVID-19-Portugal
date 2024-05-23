import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df_monthly = df.resample('M').agg({
    'total_tests': 'max',
    'new_tests': 'sum',
    'positive_rate': 'mean'
})

df_monthly = df_monthly[:22]

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_monthly.index, y=df_monthly['total_tests'],
                         mode='lines+markers',
                         name='Number of total tests performed',
                         line=dict(color='blue', width=2)))

fig.add_trace(go.Scatter(x=df_monthly.index, y=df_monthly['new_tests'],
                         mode='lines+markers',
                         name='Number of newly performed tests',
                         line=dict(color='green', width=2)))

fig.add_trace(go.Scatter(x=df_monthly.index, y=df_monthly['positive_rate'],
                         mode='lines+markers',
                         name='Positive Rate',
                         line=dict(color='red', width=2),
                         yaxis='y2'))

fig.update_layout(
    title='COVID-19 Testing Trends in Portugal',
    xaxis_title='Date',
    yaxis_title='Number of Tests',
    legend_title='Legend',
    template='plotly_white',
    legend=dict(
        x=1.1,
        y=1,
        xanchor='right',
        yanchor='top'
    )
)


fig.update_layout(yaxis2=dict(
    title='Positive Rate (%)',
    overlaying='y',
    side='right'
))

fig.update_traces(
    hoverinfo='name+y+x'
)

fig.update_xaxes(
    tickformat="%d.%m.%Y",
    ticklabelmode="period"
)

fig.write_html('../plots/6_tests.html')
