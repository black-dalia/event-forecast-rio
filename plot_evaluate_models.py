import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from RNN_preproc_uni import get_train_test
from metrics import forecast_accuracy, get_baseline_data
import  preproc_RNN_LSTM
from baseline import get_baseline_predictions, forecast_accuracy



def compute_plot_pred(data,modelname,AR, nseq, length):
    ''' for 1 to 1 model'''
    '''compute and plot prediction over test time period and overlay with actual data'''
    y_pred = []
    len_ = int(0.8*data.shape[0])
    data_test = data[len_:]
    for i in range(int((804-(length-31))/31)+1):
      data_test_temp = data_test[i*31:i*31+(length-31)]
      data_test_temp = data_test_temp[AR]
      data_test_temp = np.array(data_test_temp)
      data_test_temp = data_test_temp.reshape(1,(length-31),1)
      y_pred_temp = modelname.model.predict(data_test_temp).tolist()[0]
      y_pred = y_pred + y_pred_temp

    y_pred_df = pd.DataFrame(y_pred)
    y_pred_df["index"] = y_pred_df.index + 3214+(length-31) # create index that will match input table
    y_pred_df = y_pred_df.set_index("index")
    actual = data_test[(length-31):]# take first predicted value from actual data until the end
    actual =actual[AR]

    plt.figure(figsize=(16,6))
    plt.plot(actual, c= "blue")
    plt.plot(y_pred_df, c="red")

    _, _, X_test, y_test = get_train_test(data,nseq,length, AR)
    res = modelname.evaluate(X_test, y_test, verbose=0)
    print(f"performances computed on test set:{res}")
    return y_pred

def compute_plot_pred_multi(data,modelname,length, prediction_horizon):
    ''' for many to many model'''
    '''compute and plot prediction over test time period and overlay with actual data'''
    data_wo_date = data.drop(columns="Date")
    len_ = int(0.8*data_wo_date.shape[0])
    data_test = data_wo_date[len_:]
    y_pred= []
    for i in range(int((804-(length-prediction_horizon))/prediction_horizon)+1):
        data_test_temp = data_test[i*prediction_horizon:i*prediction_horizon+(length-prediction_horizon)]
        data_test_temp = np.array(data_test_temp)
        data_test_temp = data_test_temp.reshape(1,(length-prediction_horizon),30)
        y_pred_temp = modelname.predict(data_test_temp).tolist()[0]
        y_pred = y_pred + y_pred_temp

    y_pred_df = pd.DataFrame(y_pred, columns = data_wo_date.columns)
    y_pred_df["index"] = y_pred_df.index + 3214+(length-prediction_horizon)
    y_pred_df = y_pred_df.set_index("index")

    actual = data_test[(length-prediction_horizon):]# take first predicted value from actual data until the end
    y_pred_df = y_pred_df[:actual.shape[0]] # only keep where there is actual data

    #get the baseline
    baseline = get_baseline_predictions(data)[(length-prediction_horizon):]
    baseline.reset_index(inplace=True)
    baseline["index"] = baseline.index + 3214+(length-prediction_horizon)
    baseline = baseline.set_index("index")

    fig, ax = plt.subplots(30,1,figsize=(16,100))
    for i,AR in enumerate(data_wo_date.columns.tolist()):
        ax[i].plot(actual[AR], c= "blue", label='actual')
        ax[i].plot(y_pred_df[AR], c="red", label = "forecast")
        ax[i].plot(baseline[AR], c="green", linestyle='dashed', label = "baseline")
        ax[i].title.set_text(AR)
        ax[i].legend(loc="upper left")

    error_pred = forecast_accuracy(actual,y_pred_df)
    error_baseline = forecast_accuracy(actual,baseline)
    print(f"Prediction MSE (computed on test set):{error_pred['mse']}")
    print(f"Baseline MSE (computed on test set):{error_baseline['mse']}")

    return y_pred_df
