from fbprophet import Prophet
import pandas as pd
import preproc
import clean
import matplotlib.pyplot as plt



def prophet_AR(df, AR):
    ts = preproc.extract_ts(df,AR)
    X_train = ts[ts["ds"].dt.year<2019]
    #y_test = ts[ts["ds"].dt.year>=2019]
    #y_test = y_test[y_test["ds"].dt.month>=2]

    model = Prophet(interval_width=0.95,
                 seasonality_mode='multiplicative')
    model.add_country_holidays(country_name='BR')
    model.fit(X_train)
    future = model.make_future_dataframe(periods=31)

    y_pred = model.predict(future)

    plt.figure(figsize=(16,6))
    plt.plot(pd.concat([ts.set_index("ds")["y"],y_pred.set_index("ds")["yhat"]],axis=1))

if __name__ == "__main__":
    data1, data2, data3, data4 = clean.get_data()
    data = clean.clean_all(data1, data2, data3, data4, clean.get_bairros_data())
    _, df = preproc.get_format(data)
    prophet_AR("Centro", df)
