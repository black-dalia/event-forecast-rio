# Import section
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import unidecode
import fuzzymatcher
from datetime import datetime

def get_data():

    data1 = pd.read_csv('raw_data/parte1.csv', sep=';', encoding = 'iso-8859-1')
    data2 = pd.read_csv('raw_data/parte2.csv', sep=';', encoding = 'iso-8859-1')
    data3 = pd.read_csv('raw_data/parte3.csv', sep=';', encoding = 'iso-8859-1')
    data4 = pd.read_csv('raw_data/parte4.csv', sep=';', encoding = 'iso-8859-1')

    return data1, data2, data3, data4

# Import data with correct bairros and AR names
def get_bairros_data():
    bairros_all = pd.read_csv("raw_data/bairros_lista.csv", encoding="iso-8859-1")
    return bairros_all
# Cleaning function
def merge_clean(data1, data2, data3, data4):
    # Merging
    data = pd.concat([data1, data2, data3, data4]) # Merging all datasets
    # Focusing on Rio de Janeiro only
    data = data[data["municipio_fato"] == "Rio de Janeiro (Capital)"] # Filtering on Rio de Janeiro only
    # Columns transforming
    data = data[["controle", "titulo_do", "total_rbft", "cisp", "data_fato",\
        "hora_fato", "local", "bairro_fato"]] # Removing useless columns
    data.columns = ["Crime_ID", "Crime_sub_type", "Crime_type",\
        "Police_station", "Date", "Time", "Place_type", "Neighborhood"]  # Renaming columns in English
    # Date and Time preprocessing
    data = data[data["Time"] != "99"] # Removing invalid time format

    # Part added to debugging - only one part of the issue
    data = data.dropna(subset = ['Date'])

    data["Test_Date_Time"] = data["Date"] + " " + data["Time"]
    data["Date_Time"] = pd.to_datetime(data["Test_Date_Time"])

    data.drop(columns=["Date", "Time"], inplace=True) # Removing time and date columns once the Date_Time is created
    data = data[data["Date_Time"] > "2008-12-31"] # Removing irrelevant date samples

    data = data.drop_duplicates(subset="Crime_ID")
    data["Neighborhood"] = data["Neighborhood"].map(lambda x: unidecode.unidecode(x)) # Removing accents
    data = data[data["Neighborhood"] != "sem informacao"] # Removing missing values for neighborhood
    return data
# Bairra detail
def barra_replace(row):
    if row == "Barra":
        row= "Barra da Tijuca"
    return row
# Bairros/AR matching
def get_AR(data, ar_data): #data_AR should be the full table with bairros and AR
    data["Neighborhood"] = data["Neighborhood"].map(barra_replace) # Setting the good "Barra da Tijuca" name
    # Bairros matching
    bairros = pd.DataFrame(ar_data, columns=["Bairro"])
    # Creating a table with only the bairros
    bairros.set_index("Bairro")
    data = fuzzymatcher.fuzzy_left_join(data, bairros, left_on="Neighborhood",\
        right_on="Bairro") # Replacing non-standardized bairros names with standardized ones
    data = data.drop(columns=["best_match_score",\
        "__id_left", "__id_right", "Neighborhood"]) # Removing useless columns
    data.rename(columns={"Bairro": "Neighborhood"}, inplace=True)
    data = pd.merge(data,ar_data,left_on="Neighborhood",\
        right_on="Bairro",how="left").drop(columns=["Regiao","IDS","Bairro","N¼"]) # Aggreagting the right AR names to our new bairros
    data.rename(columns={"R.A": "AR"}, inplace=True)
    data = data.dropna(subset=["AR"]) # Removing lines with no bairros/AR information
    return data
# Cleaning - all
def clean_all(data1, data2, data3, data4, ar_data):
    data = merge_clean(data1, data2, data3, data4)
    data = get_AR(data, ar_data)
    return data


if __name__ == "__main__":
    print("start time  =", datetime.now())
    data1, data2, data3, data4 = get_data()
    data = clean_all(data1, data2, data3, data4, get_bairros_data())
    print(data.head(5))
    print("end time  =", datetime.now())
