import pandas as pd

def get_popfile():
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
    pop_data = clean_pop_data()
    print(pop_data.head(30))
