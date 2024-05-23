import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
import plotly.graph_objects as go
import plotly.io as pio

df = pd.read_csv('../data/portugal.csv')

data = df[['date', 'new_cases', 'new_deaths', 'reproduction_rate', 'icu_patients', 'hosp_patients', 'new_tests', 'positive_rate', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters', 'stringency_index', 'excess_mortality_cumulative_absolute', 'excess_mortality_cumulative', 'excess_mortality']]

data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)
weekly_data = data.resample('W').sum()

weekly_data = weekly_data.loc[:'2022-06-12']

X = weekly_data.drop(columns=['new_deaths'])
y = weekly_data['new_deaths']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)
    return predictions, mae, rmse, r2

models = {
    'Linear Regression': LinearRegression(),
    'LASSO': GridSearchCV(Lasso(), {'alpha': [0.01, 0.1, 1, 10]}, cv=5, scoring='neg_mean_squared_error'),
    'Ridge': GridSearchCV(Ridge(), {'alpha': [0.01, 0.1, 1, 10]}, cv=5, scoring='neg_mean_squared_error'),
    'ElasticNet': GridSearchCV(ElasticNet(), {'alpha': [0.01, 0.1, 1, 10], 'l1_ratio': [0.1, 0.5, 0.9]}, cv=5, scoring='neg_mean_squared_error'),
    'Random Forest': GridSearchCV(RandomForestRegressor(random_state=42), {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }, cv=5, scoring='neg_mean_squared_error'),
    'Decision Tree': GridSearchCV(DecisionTreeRegressor(random_state=42), {
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }, cv=5, scoring='neg_mean_squared_error'),
    'Gradient Boosting': GridSearchCV(GradientBoostingRegressor(random_state=42), {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, 10],
        'min_samples_split': [2, 5, 10]
    }, cv=5, scoring='neg_mean_squared_error'),
    'AdaBoost': GridSearchCV(AdaBoostRegressor(random_state=42), {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 1]
    }, cv=5, scoring='neg_mean_squared_error'),
    'XGBoost': GridSearchCV(XGBRegressor(random_state=42), {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.1, 1]
    }, cv=5, scoring='neg_mean_squared_error'),
    'CatBoost': GridSearchCV(CatBoostRegressor(random_state=42, verbose=0), {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.1, 1]
    }, cv=5, scoring='neg_mean_squared_error'),
    'KNN': GridSearchCV(KNeighborsRegressor(), {
        'n_neighbors': [3, 5, 7, 10],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }, cv=5, scoring='neg_mean_squared_error')
}

results = {}
predictions_dict = {}

for name, model in models.items():
    start_time = time.time()
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    if isinstance(model, GridSearchCV):
        models[name] = model.best_estimator_
        predictions, mae, rmse, r2 = evaluate_model(models[name], X_test, y_test)
        results[name] = (mae, rmse, r2)
        predictions_dict[name] = predictions
    else:
        predictions, mae, rmse, r2 = evaluate_model(model, X_test, y_test)
        results[name] = (mae, rmse, r2)
        predictions_dict[name] = predictions

    print(f"{name} trained in {time.time() - start_time:.2f} seconds.")
    print(f"{name}: MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

feature_importances = {}

for name, model in models.items():
    if name in ['Linear Regression', 'LASSO', 'Ridge', 'ElasticNet']:
        feature_importances[name] = model.coef_
    elif name in ['Random Forest', 'Gradient Boosting', 'AdaBoost', 'XGBoost', 'CatBoost', 'Decision Tree']:
        feature_importances[name] = model.feature_importances_
    elif name == 'KNN':
        result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
        feature_importances[name] = result.importances_mean

feature_importances_df = pd.DataFrame(feature_importances, index=X.columns)

feature_importances_df.to_csv('../data/10_feature_importances.csv')

results_df = pd.DataFrame(results, index=['MAE', 'RMSE', 'R2'])

results_df.to_csv('../data/10_results.csv')

plt.figure(figsize=(14, 7))
plt.plot(y_test.values, label='True Values', color='black', linewidth=2)

for model_name, predictions in predictions_dict.items():
    plt.plot(predictions, label=f"{model_name}, MAE: {results[model_name][0]:.2f}, RMSE: {results[model_name][1]:.2f}, R2: {results[model_name][2]:.2f}", alpha=0.7)

plt.legend()
plt.xlabel('Sample Index')
plt.ylabel('New Deaths')
plt.title('Predicted vs True Values of New Deaths')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig('../plots/10_predicted_vs_true_values.png')

true_values_trace = go.Scatter(
    x=list(range(len(y_test))),
    y=y_test.values,
    mode='lines',
    name='True Values',
    line=dict(color='black', width=2)
)

data = [true_values_trace]

for model_name, predictions in predictions_dict.items():
    mae = results[model_name][0]
    rmse = results[model_name][1]
    r2 = results[model_name][2]
    model_trace = go.Scatter(
        x=list(range(len(predictions))),
        y=predictions,
        mode='lines',
        name=f"{model_name}, MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}",
        opacity=0.7
    )
    data.append(model_trace)

layout = go.Layout(
    title='Predicted vs True Values of New Deaths',
    xaxis=dict(title='Sample Index'),
    yaxis=dict(title='New Deaths'),
    template='plotly_white',
    legend=dict(
        x=1.1,
        y=1,
        xanchor='right',
        yanchor='top'
    )
)

fig = go.Figure(data=data, layout=layout)

pio.write_html(fig, file='../plots/10_predicted_vs_true_values.html')
