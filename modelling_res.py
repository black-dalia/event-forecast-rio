import pandas as pd
import numpy as np


def compute_plot_pred(data,AR,length):
  '''compute and plot prediction over test time period and overlay with actual data'''
  y_pred = []
  len_ = int(0.8*data.shape[0])
  data_test = data[len_:]
  for i in range(int((804-(length-31))/31)+1):
    data_test_temp = data_test[i*31:i*31+(length-31)]
    data_test_temp = data_test_temp[AR]
    data_test_temp = np.array(data_test_temp)
    data_test_temp = data_test_temp.reshape(1,(length-31),1)
    y_pred_temp = history.model.predict(data_test_temp).tolist()[0]
    y_pred = y_pred + y_pred_temp

  y_pred_df = pd.DataFrame(y_pred)
  y_pred_df["index"] = y_pred_df.index + 3214+(length-31) # create index that will match input table
  y_pred_df = y_pred_df.set_index("index")
  actual = data_test[(length-31):]# take first predicted value from actual data until the end
  actual =actual[AR]

  plt.figure(figsize=(16,6))
  plt.plot(actual, c= "blue")
  plt.plot(y_pred_df, c="red")

  _, _, X_test, y_test = get_train_test(data,2000,length, AR)
  res = model.evaluate(X_test, y_test, verbose=0)
  print(f"performances computed on test set:{res}")
  return y_pred
