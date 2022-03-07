import numpy as np
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt


def get_baseline_actual(df):
    '''validation period: 2017-10-19 incl to 2019-12-31 incl'''
    #df = df.droplevel(level=0,axis=1).reset_index()
    baseline_month_actual = df[(df['Date'] >= "2017-10-19") \
        & (df['Date']<= "2019-12-31")].reset_index().drop(columns="index")
    return baseline_month_actual

def get_baseline_predictions(df):
    '''compute baseline model (mean) for the validation period'''
    #df = df.droplevel(level=0,axis=1).reset_index()
    baseline_data = df[(df['Date'] >= "2016-10-19") & (df['Date'] < "2017-10-19")]
    baseline_data = baseline_data.reset_index().drop(columns="index")
    baseline_mean = baseline_data.mean().to_frame().T
    baseline_month_forecast = pd.concat([baseline_mean]*804).reset_index().drop(columns="index")
    return baseline_month_forecast

def forecast_accuracy(actual, forecast):

    forecast = forecast.to_numpy()
    actual = actual.to_numpy()
    #mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    #mpe = np.mean((forecast - actual)/actual)   # MPE
    mse = np.mean(np.square(forecast - actual))
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    #mins = np.amin(np.hstack([forecast[:,None],
    #                          actual[:,None]]), axis=1)
    #maxs = np.amax(np.hstack([forecast[:,None],
     #                         actual[:,None]]), axis=1)
    #minmax = 1 - np.mean(mins/maxs)             # minmax
    #acf1 = acf(fc-test)[1]                      # ACF1
    return({#'mape':mape,
            'mse':mse,
            'mae': mae,
            #'mpe': mpe,
            #'rmse':rmse, #'acf1':acf1,
            'corr':corr,
            #'minmax':minmax
            })

# Note: Make sure to pass the region in quotation marks, such as "Mare" or "Anchieta"
def get_baseline_metrics(df, AR):
    baseline_month_actual_region = get_baseline_actual(df)[AR]
    baseline_month_forecast_region = get_baseline_predictions(df)[AR]

    baseline_metrics = forecast_accuracy(baseline_month_forecast_region, baseline_month_actual_region)
    return baseline_metrics

def baseline_plt(df,AR):
    actual =get_baseline_actual(df)
    baseline = get_baseline_predictions(df)
    plt.figure(figsize=(16,6))
    plt.plot(actual.Date, actual[AR])
    plt.plot(actual.Date, baseline[AR])
