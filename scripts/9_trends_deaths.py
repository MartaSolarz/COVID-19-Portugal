import pandas as pd
from neuralprophet import NeuralProphet
from neuralprophet import set_random_seed
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt

data = pd.read_csv('./data/portugal.csv')

df = pd.DataFrame()
df['ds'] = pd.to_datetime(data['date'], format='%Y-%m-%d', errors='coerce')
df['y'] = data['new_deaths']

df = df[df['y'] > 0]

period1 = df[(df['ds'] >= '2020-01-01') & (df['ds'] < '2023-01-01')]
period2 = df[(df['ds'] >= '2023-01-01') & (df['ds'] <= '2025-01-01')]

# Forecast for the first period
set_random_seed(1234)
nm1 = NeuralProphet(n_changepoints=190,
                    daily_seasonality=True,
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    changepoints_range=0.95,
                    seasonality_mode='additive',
                    trend_reg=0.3,
                    seasonality_reg=0.2 )

nm_result = nm1.fit(period1, freq='D')
future = nm1.make_future_dataframe(period1, periods=1500, n_historic_predictions=len(period1))
forecast_1 = nm1.predict(future)

forecast_1['yhat1'] = forecast_1['yhat1'].apply(lambda x: max(0, x))

# Forecast for the second period
nm2 = NeuralProphet(n_changepoints=200,
                    daily_seasonality=True,
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    changepoints_range=0.95)

nm_result2 = nm2.fit(period2, freq='D')
future2 = nm2.make_future_dataframe(period2, periods=1000, n_historic_predictions=len(period2))
forecast_2 = nm2.predict(future2)

forecast_2['yhat1'] = forecast_2['yhat1'].apply(lambda x: max(0, x))

overlap_forecast = forecast_1[forecast_1['ds'] <= period1['ds'].max()]
future_forecast = forecast_1[forecast_1['ds'] > period1['ds'].max()]

overlap_forecast2 = forecast_2[forecast_2['ds'] <= period2['ds'].max()]
future_forecast2 = forecast_2[forecast_2['ds'] > period2['ds'].max()]

# Two forecasts in one plot
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='lines',
                         name='observed data', line=dict(color='black')))

fig.add_trace(go.Scatter(x=overlap_forecast['ds'], y=overlap_forecast['yhat1'], mode='lines',
                         name='forecast based on period 2020-2022 (overlap)', line=dict(color='orange'), opacity=0.6))

fig.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat1'], mode='lines',
                         name='forecast based on period 2020-2022', line=dict(color='orange')))

fig.add_trace(go.Scatter(x=overlap_forecast2['ds'], y=overlap_forecast2['yhat1'], mode='lines',
                         name='forecast based on period 2023-2024 (overlap)', line=dict(color='red'), opacity=0.6))

fig.add_trace(go.Scatter(x=future_forecast2['ds'], y=future_forecast2['yhat1'], mode='lines',
                         name='forecast based on period 2023-2024', line=dict(color='red')))

fig.update_layout(title='Forecast of new COVID-19 deaths in Portugal',
                  xaxis_title='Date',
                  yaxis_title='New Deaths',
                  template='plotly_white',
                  showlegend=True,
                  hovermode='x unified',
                  legend=dict(
                      x=0.7,
                      y=0.99,
                      xanchor='left',
                      yanchor='top',
                      bgcolor='rgba(255, 255, 255, 0.5)',
                      bordercolor='rgba(0, 0, 0, 0.5)',
                      borderwidth=1
                  ))

pio.write_html(fig, file="./plots/9_deaths_forecast.html", auto_open=True)

# Forecast plot for the first period
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=period1['ds'], y=period1['y'], mode='lines', name='observed', line=dict(color='black')))

fig1.add_trace(go.Scatter(x=overlap_forecast['ds'], y=overlap_forecast['yhat1'], mode='lines',
                         name='forecats (overlap)', line=dict(color='orange'), opacity=0.6))

fig1.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat1'], mode='lines',
                         name='forecast', line=dict(color='orange')))

fig1.update_layout(title='Prediction based on first period: 2020-2022',
                   xaxis_title='Date',
                   yaxis_title='New Deaths',
                   template='plotly_white',
                   hovermode='x'
                   )

fig1.update_xaxes(tickformat="%d.%m.%Y",
                  ticklabelmode="period")

fig1.update_traces(
    hoverinfo='name+y+x'
)

fig1.write_html("../plots/9_deaths_period1_forecast.html")

# Forecast plot for the second period
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=period2['ds'], y=period2['y'], mode='lines', name='observed', line=dict(color='black')))

fig2.add_trace(go.Scatter(x=overlap_forecast2['ds'], y=overlap_forecast2['yhat1'], mode='lines',
                         name='forecats (overlap)', line=dict(color='red'), opacity=0.6))

fig2.add_trace(go.Scatter(x=future_forecast2['ds'], y=future_forecast2['yhat1'], mode='lines',
                         name='forecast', line=dict(color='red')))

fig2.update_layout(title='Prediction based on second period: 2023-2024',
                   xaxis_title='Date',
                   yaxis_title='New Deaths',
                   template='plotly_white',
                   hovermode='x')

fig2.write_html("./plots/9_deaths_period2_forecast.html")

# Static plot

fig, axs = plt.subplots(3, 1, figsize=(15, 15), gridspec_kw={'height_ratios': [1.5, 1, 1]})

axs[0].plot(df['ds'], df['y'], label='Observed', color='black')
axs[0].plot(overlap_forecast['ds'], overlap_forecast['yhat1'], label='Forecast 2020-2022 (overlap)', color='orange', alpha=0.6)
axs[0].plot(overlap_forecast2['ds'], overlap_forecast2['yhat1'], label='Forecast 2023-2024 (overlap)', color='red', alpha=0.6)
axs[0].plot(future_forecast['ds'], future_forecast['yhat1'], label='Forecast 2020-2022', color='orange')
axs[0].plot(future_forecast2['ds'], future_forecast2['yhat1'], label='Forecast 2023-2024', color='red')
axs[0].set_title('Forecast of New COVID-19 Deaths in Portugal (NeuralProphet)')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('New Deaths')
axs[0].grid(True, which='both', linestyle='--', lw=0.5)
axs[0].legend()

axs[1].plot(period1['ds'], period1['y'], label='Observed', color='black')
axs[1].plot(overlap_forecast['ds'], overlap_forecast['yhat1'], label='Forecast 2020-2022 (overlap)', color='orange', alpha=0.6)
axs[1].plot(future_forecast['ds'], future_forecast['yhat1'], label='Forecast 2020-2022', color='orange')
axs[1].set_title('Prediction Based on First Period: 2020-2022')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('New Deaths')
axs[1].grid(True, which='both', linestyle='--', lw=0.5)
axs[1].legend()

axs[2].plot(period2['ds'], period2['y'], label='Observed', color='black')
axs[2].plot(overlap_forecast2['ds'], overlap_forecast2['yhat1'], label='Forecast 2023-2024 (overlap)', color='red', alpha=0.6)
axs[2].plot(future_forecast2['ds'], future_forecast2['yhat1'], label='Forecast 2023-2024', color='red')
axs[2].set_title('Prediction Based on Second Period: 2023-2024')
axs[2].set_xlabel('Date')
axs[2].set_ylabel('New Deaths')
axs[2].grid(True, which='both', linestyle='--', lw=0.5)
axs[2].legend()

plt.tight_layout()
plt.savefig('../plots/9_combined_forecast_deaths.png', dpi=300)