from metrics import get_baseline_data
import numpy as np
import math
import tensorflow
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras import optimizers, metrics
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import RobustScaler

## Notes for group members:
# Attention: This model is fitted with a regular validation set. We should actually adjust it in a way that the validation
# set consists of a number of randomly selected sequences.
# On March 4, this model was also uploaded to Google Drive.
# To get the model from Google drive, see the corresponding link in the slack group.

#data = get_baseline_data("raw_data/preproc_data_rate.csv")
#data_wo_date = data.drop(columns="Date")

def subsample_sequence(data, length): # Return a shorter dataframe with specified length
    last_possible = data.shape[0] - length
    random_start = np.random.randint(0, last_possible)
    data_sample = data[random_start: random_start+length]
    return data_sample

def split_subsample_sequence(data, length, prediction_horizon): # Return a random sequence of specified length
    data_subsample = subsample_sequence(data, length)
    y_sample = data_subsample.iloc[length-prediction_horizon:]

    X_sample = data_subsample[0:length-prediction_horizon]
    X_sample = X_sample.values
    return np.array(X_sample), np.array(y_sample)

def get_X_y(data, n_sequences, length, prediction_horizon): # Return a sepcific number of (X,y) samples of specified length for all adm. regions

    X, y = [], []

    for i in range(n_sequences):
        (xi, yi) = split_subsample_sequence(data, length, prediction_horizon)
        X.append(xi)
        y.append(yi)

    X = np.array(X)
    y = np.array(y)
    return X, y

def get_train_test(data,n_sequences,length, prediction_horizon): # Return train and test data
    data_wo_date = data.drop(columns="Date")

    len_ = int(0.8*data_wo_date.shape[0])
    data_train = data_wo_date[:len_]
    data_test = data_wo_date[len_:]

    test_seq = math.floor(n_sequences/4)

    X_train, y_train = get_X_y(data_train, n_sequences, length,prediction_horizon)
    X_test, y_test = get_X_y(data_test, test_seq, length, prediction_horizon)

#     X_train = X_train.reshape(X_train.shape[0], X_train.shape[1],1)
#     X_test = X_test.reshape(X_test.shape[0], X_test.shape[1],1)

    return X_train, y_train, X_test, y_test

def model(number_of_sequences, input_sequence_length, number_of_regions, prediction_horizon):
# number_of_sequences = 1000 # number of data sequences for training
# input_sequence_length = 169 # sequence length in training process
# number_of_regions = 30 # number of region sin training process
# prediction_horizon = 31 # number of predicted days by region
#X_train_shape = (number_of_sequences, input_sequence_length, number_of_regions)
#y_train_shape = (number_of_sequences, input_sequence_length, number_of_regions)

    model = models.Sequential()
    model.add(layers.LSTM(40, return_sequences=False, activation="tanh", \
        input_shape = (input_sequence_length, number_of_regions)))
    model.add(layers.RepeatVector(prediction_horizon))
    model.add(layers.LSTM(40, return_sequences=True, activation="tanh"))
    model.add(layers.TimeDistributed(layers.Dense(number_of_regions,"relu")))
    model.compile(loss="mse",
                optimizer="rmsprop")
    return model

def fit_model(X_train, y_train, model):
    es = EarlyStopping(monitor='val_loss', verbose=1, patience=20, restore_best_weights=True)
    hist = model.fit(X_train, y_train, callbacks=[es],epochs = 2000,validation_split =0.3, batch_size=32)
    return hist
