# Import section
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from clean import clean_all, get_data, get_bairros_data

# Function taking a clean dataset and returning it with ARIMA-suited format
def get_format(data):
    data['Date'] = data['Date_Time'].dt.date
    preprocessed_data = data.groupby(['RA', 'Date']).count()[['Crime_ID']]
    preprocessed_data.rename(columns={'Crime_ID':'nb_crimes'}, inplace=True)
    preprocessed_data = preprocessed_data.unstack(level=0)
    preprocessed_data = preprocessed_data.replace(np.nan, 0).astype(int)

    return preprocessed_data

if __name__ == "__main__":
    data1, data2, data3, data4 = get_data()
    data = clean_all(data1, data2, data3, data4, get_bairros_data())
    preprocessed_data = get_format(data)
    print(preprocessed_data.tail(10))
