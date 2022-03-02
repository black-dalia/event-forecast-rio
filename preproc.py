# Import section
from datetime import datetime
from webbrowser import get
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from clean import clean_all, get_data, get_bairros_data

def get_format(data):
    '''Function taking a clean dataset and returning 2 ARIMA-friendly df:
    1. total nb_crime / day and AR
    2. nb_crime per 1000 inhab / day and AR'''

    data["Date"] = data["Date_Time"].dt.date
    preprocessed_data = data.groupby(["AR", "Date"]).count()[["Crime_ID"]]
    preprocessed_data.rename(columns={"Crime_ID":"nb_crimes"}, inplace=True)

    ## add a column with yearly population per AR
    pop_clean = clean_pop_data()
    preprocessed_data["year_temp"] = preprocessed_data.index.map(lambda x: x[1].year)
    input_merge = preprocessed_data.reset_index()
    data_merge = pd.merge(left=input_merge, right=pop_clean, left_on=["AR","year_temp"],\
        right_on=["administrative_regions", "Ano"])
    data_merge.drop(columns=["administrative_regions","Ano"], inplace = True)
    preprocessed_data.drop(columns=["year_temp"],inplace = True)
    ## compute nb crimes / 1000 inhabitants
    data_merge["nb_crimes_1000"]=data_merge.nb_crimes / data_merge.Populacao*1000
    data_merge.drop(columns=["nb_crimes","Populacao","year_temp"], inplace=True)
    data_merge.set_index(["AR","Date"],inplace=True)
    ##
    preprocessed_data = preprocessed_data.unstack(level=0)
    preprocessed_data = preprocessed_data.replace(np.nan, 0).astype(int)
    preprocessed_data_1000 = data_merge.unstack(level=0)
    preprocessed_data_1000 = preprocessed_data_1000.replace(np.nan, 0)
    return preprocessed_data, preprocessed_data_1000

def get_popfile():
    '''import population file'''
    return pd.read_csv("raw_data/population_Rio.csv", sep=",")

def clean_pop_data():
    data= get_popfile()
    data = data.drop(columns=["DensidadeBruta", "DensidadeLiquida", "TaxaGeometrica"])

    # Get rid of Roman numbers in front of name of administrative regions
    splitted_regions = data['RegiaoAdministrativa'].str.split().str[1:]
    cleaned_regions = splitted_regions.str.join(" ")
    data["administrative_regions"] = cleaned_regions
    data = data.drop(columns=["RegiaoAdministrativa"])

    # Dictionary of population data per region for 2000-2020 in 5-years steps
    regions_dict = {}
    for region in data["administrative_regions"].unique():
        regions_dict[region] = data[data["administrative_regions"]==region]

    # Dataframe with years for 2000-2020 in 1-year steps
    year_df = pd.DataFrame(pd.period_range(min(data.Ano), max(data.Ano), freq="Y"), columns=["Ano"])
    year_df = year_df[["Ano"]].astype("str").astype("int64")

    # Extend time series to annual time series and interpolate lineraly the missing population data
    middle_dict = {}
    for k, v in regions_dict.items():
        middle_dict[k] = year_df.merge(v, how="left", on="Ano")
        middle_dict[k]["administrative_regions"].fillna(value=k, inplace=True)
        middle_dict[k]["Populacao"].interpolate(method='linear', inplace=True)


    # Create a new dataframe with cleand and extended population data
    empty = pd.DataFrame(columns=["Ano", "Populacao", "administrative_regions"])
    df = pd.concat(middle_dict).reset_index().drop(columns=["level_0", "level_1"])

    return df

if __name__ == "__main__":
    print("start time  =", datetime.now())
    data1, data2, data3, data4 = get_data()
    data = clean_all(data1, data2, data3, data4, get_bairros_data())
    preprocessed_data, preprocessed_data_1000 = get_format(data)
    pop_clean = clean_pop_data()
    print(pop_clean.head())
    print(preprocessed_data.tail(10))
    print(preprocessed_data_1000.tail(10))

    print("end time  =", datetime.now())
