import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/portugal.csv', parse_dates=['date'], index_col='date')
df.fillna(0, inplace=True)

df = df[df['new_deaths'] > 0]
df = df[:'2022-02-28']

fig = go.Figure()

fig.add_trace(go.Bar(x=df.index, y=df['icu_patients'], name='ICU Patients', marker_color='red'))
fig.add_trace(go.Bar(x=df.index, y=df['hosp_patients'], name='Hospital Patients', marker_color='blue'))
fig.add_trace(go.Bar(x=df.index, y=df['new_deaths'], name='New Weekly Deaths', marker_color='black'))

fig.update_layout(
    title='ICU, Hospital Patients and Weekly Deaths due to COVID-19 in Portugal',
    xaxis_title='Date',
    yaxis_title='Number of Patients / Deaths',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    barmode='group'
)

fig.write_html('../plots/8_hospitals_interactive.html')
