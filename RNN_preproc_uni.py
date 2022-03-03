import math
import pandas as pd
import numpy as np


def subsample_sequence(df, length):
    """
    Given the initial dataframe `df`, return a shorter dataframe sequence of length `length`.
    This shorter sequence should be selected at random
    """
    last_possible = df.shape[0] - length

    random_start = np.random.randint(0, last_possible)
    df_sample = df[random_start: random_start+length]

    return df_sample

def split_subsample_sequence(df, length):
    '''Create one single random (X,y) pair'''
    df_subsample = subsample_sequence(df, length)
    pred_len = 31
    y_sample = df_subsample.iloc[length-pred_len:]

    X_sample = df_subsample[0:length-pred_len]
    X_sample = X_sample.values
    return np.array(X_sample), np.array(y_sample)

def get_X_y(df, n_sequences, length):
    '''Return a list of samples (X, y)'''
    X, y = [], []

    for i in range(n_sequences):
        (xi, yi) = split_subsample_sequence(df, length)
        X.append(xi)
        y.append(yi)

    X = np.array(X)
    y = np.array(y)
    return X, y

def get_train_test(df,n_sequences,length):
    '''Returns train and test data for X and y'''
    len_ = int(0.8*df.shape[0])
    df_train = df[:len_]
    df_test = df[len_:]

    test_seq = math.floor(n_sequences/4)

    X_train, y_train = get_X_y(df_train, n_sequences, length)
    X_test, y_test = get_X_y(df_test, test_seq, length)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1],1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1],1)

    return X_train, y_train, X_test, y_test

#input
#Centro_df = preproc.extract_ts(preproc_data_rate,"Centro")["y"]

#output
#X_train, y_train, X_test, y_test = get_train_test(Centro_df, 200, 21)
