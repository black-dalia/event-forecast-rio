import numpy as np
import pandas as pd

# Baseline model predicts daily values of crime per 1000 inhabitants per region for 2019 based on the
# annual mean of crime per 1000 inhabitants per region for 2018.
# Prediction horizon is one month, we are predicting daily values for January 2021 (31 days).

def get_baseline_data(path):
    # Preprocessing of baseline data
    df = pd.read_csv(path)
    df.columns = ["Date", "Anchieta", "Bangu", "Barra da Tijuca", "Botafogo",
       "Campo Grande", "Centro", "Cidade de Deus", "Complexo do Alemao",
       "Copacabana", "Guaratiba", "Ilha do Governador", "Inhauma", "Iraja",
       "Jacarepagua", "Jacarezinho", "Lagoa", "Madureira", "Mare", "Meier",
       "Pavuna", "Portuaria", "Ramos", "Realengo", "Rio Comprido", "Rocinha",
       "Santa Cruz", "Santa Teresa", "Sao Cristovao", "Tijuca", "Vila Isabel"]
    df = df.iloc[2:-1]
    df = df.reset_index().drop(columns="index")
    df["Date"] = pd.to_datetime(df.Date)
    region_columns = list(df.columns)[1:]
    for column in region_columns:
        df[column] = pd.to_numeric(df[column])
    return df

# From the function below you can select the column of the required region to obtain y_pred_baseline.
# This can then be passed to the forecast_accuracy function as "forecast".

def get_baseline_actual(df):
    baseline_month_actual = df[(df['Date'] >= "2019-01-01") & (df['Date'] < "2019-02-01")].reset_index().drop(columns="index")
    return baseline_month_actual

def get_baseline_predictions(df):
    baseline_data = df[(df['Date'] >= "2018-01-01") & (df['Date'] < "2019-01-01")]
    baseline_data = baseline_data.reset_index().drop(columns="index")
    baseline_mean = baseline_data.mean().to_frame().T
    baseline_month_forecast = pd.concat([baseline_mean]*31).reset_index().drop(columns="index")
    return baseline_month_forecast

def forecast_accuracy(forecast, actual):
    forecast = forecast.to_numpy()
    actual = actual.to_numpy()
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None],
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None],
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    #acf1 = acf(fc-test)[1]                      # ACF1
    return({'mape':mape, 'me':me, 'mae': mae,
            'mpe': mpe, 'rmse':rmse, #'acf1':acf1,
            'corr':corr, 'minmax':minmax})

# Note: Make sure to pass the region in quotation marks, such as "Mare" or "Anchieta"
def get_baseline_metrics(region, df):
    baseline_month_actual_region = get_baseline_actual(df)[region]
    baseline_month_forecast_region = get_baseline_predictions(df)[region]

    baseline_metrics = forecast_accuracy(baseline_month_forecast_region, baseline_month_actual_region)
    return baseline_metrics

# How to run this file entirely:
    # df = get_baseline_data(path)
    # baseline_month_forecast = get_baseline_predictions(df)
    # baseline_month_actual = get_baseline_actual(df)
    # baseline_metrics = get_baseline_metrics(region, df)
