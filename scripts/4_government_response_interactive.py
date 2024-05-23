import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/portugal.csv', index_col='date', parse_dates=True)
df.fillna(0, inplace=True)

df = df.resample('M').agg({
    'new_cases': 'sum',
    'new_deaths': 'sum',
    'stringency_index': 'mean'
})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df['new_cases'],
                         mode='lines+markers',
                         name='New Cases',
                         line=dict(color='blue', width=2)))

fig.add_trace(go.Scatter(x=df.index, y=df['new_deaths'],
                         mode='lines+markers',
                         name='New Deaths',
                         line=dict(color='red', width=2)))

fig.add_trace(go.Scatter(x=df.index, y=df['stringency_index'],
                         mode='lines+markers',
                         name='Stringency Index',
                         line=dict(color='green', width=2),
                         yaxis='y2'))

fig.update_layout(
    title='COVID-19 Government Response in Portugal',
    title_font=dict(size=20, family='Arial', color='black'),
    xaxis_title='Date',
    yaxis=dict(
        title='Number of Cases/Deaths',
        rangemode='tozero'
    ),
    yaxis2=dict(
        title='Stringency Index',
        overlaying='y',
        side='right',
        range=[0, 100]
    ),
    template='plotly_white',
    legend_title='Legend',
    hovermode='x',
    legend=dict(
        x=1.3,
        y=1,
        xanchor='right',
        yanchor='top'
    )
)

fig.update_traces(
    hoverinfo='name+y+x'
)

fig.update_xaxes(
    tickformat="%d.%m.%Y",
    ticklabelmode="period"
)

fig.write_html('../plots/4_government_response_interactive.html')
