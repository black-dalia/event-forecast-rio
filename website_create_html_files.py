from metrics import get_baseline_data
from baseline import get_baseline_predictions
from tensorflow.keras import models
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import unidecode

data = get_baseline_data("raw_data/preproc_data_rate.csv")
new_model = models.load_model("/home/aklein21/code/Goldmariek/event-forecast-rio/RNN_LSTM")

def get_pred_actual_baseline(data,modelname,length, prediction_horizon):
    ''' for many to many model'''
    '''compute and plot prediction over test time period and overlay with actual data'''
    data_wo_date = data.drop(columns="Date")
    len_ = int(0.8*data_wo_date.shape[0])
    data_test = data_wo_date[len_:]
    y_pred= []
    for i in range(int((804-(length-prediction_horizon))/prediction_horizon)+1):
        data_test_temp = data_wo_date[i*prediction_horizon:i*prediction_horizon+(length-prediction_horizon)]
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

    return y_pred_df, baseline, actual

def append_dates(data):
    data["Date"] =pd.date_range("2018-04-06", periods=635, freq="D").date
    return data

def get_folium_dataframe(y_pred_df, actual):
    regions = list(actual.columns)[0:30]
    list_of_df = []

    for region in regions:
        df = pd.DataFrame(columns=["region", "actual", "predicted", "Date"])
        # df["baseline"] = baseline[region]
        df["actual"] = actual[region]
        df["region"] = region
        df["predicted"] = y_pred_df[region]
        df["Date"] = y_pred_df["Date"]
        list_of_df.append(df)

    map_df = pd.concat(list_of_df)
    return map_df

def get_hover_text(map_df):
    hover_text = []
    for index, row in map_df.iterrows():
        hover_text.append(('<b>{region}</b><br><br>'+
                      'Date: {Date}<br>'+
                      'Predicted Value: {predicted}<br>'+
                      'Actual Value: {actual}<br>'
                       ).format(
                       region=row['region'],
                       Date=row['Date'],
                        predicted=row["predicted"],
                       actual=row['actual']
                      ))

    map_df['text'] = hover_text
    return map_df


def create_html_files(map_df):
    figs = {} # Create an empty figure to which we will add all the plotly figures
    regions_list=[] #Create an empty list to which we will append all the cities
    html_list=[] #Create an empty list to which we will append all the exported html files
    regions = list(map_df.region.unique())
    for i, region in enumerate(regions, start = 0):
        regions_list.append(region)
        html_list.append('fig'+str(i)+'.html')
        df_region = map_df[map_df['region']==region]

        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(                           #Add the second chart (line chart) to the figure
            go.Scatter(
            x=df_region['Date'],
            y=df_region['actual'],
            name="Actual Value",
            mode='lines',
            text=df_region['text'],
            hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
            line = dict(color='firebrick', width=3)#Specify the color of the line
            ),
            secondary_y=True)

        fig.add_trace(                           #Add the second chart (line chart) to the figure
            go.Scatter(
            x=df_region['Date'],
            y=df_region['predicted'],
            name="Predicted Value",
            mode='lines',
            text=df_region['text'],
            hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
            line = dict(color='blue', width=3)#Specify the color of the line
            ),
            secondary_y=True)

        fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light gray
                    title_text="Crime Prediction and actual values: " + regions[i], #Add a chart title
                    title_font_family="Times New Roman",
                    title_font_size = 20,
                    title_font_color="darkblue", #Specify font color of the title
                    title_x=0.5, #Specify the title position
                    xaxis=dict(
                            tickfont_size=10,
                            tickangle = 270,
                            showgrid = True,
                            zeroline = True,
                            showline = True,
                            showticklabels = True,
                            dtick="M1", #Change the x-axis ticks to be monthly
                            tickformat="%b\n%Y"
                            ),
                    legend = dict(orientation = 'h', xanchor = "center", x = 0.72, y= 1), #Adjust legend position
                    yaxis_title='# Crimes per 1000')

        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
        #         dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]))
        )

        figs['fig'+str(i)] = fig
        fig.write_html('fig'+str(i)+".html")

    df1=pd.DataFrame(regions_list,columns =['regions'])
    df2=pd.DataFrame(html_list,columns =['html_file'])
    df3=pd.concat([df1, df2], axis=1)
    df3["regions"] = df3.regions.map(lambda x: x.upper())
    return df3

def get_shapes_centroids(geojson_path):
    df = gpd.read_file('raw_data/Limite_Bairro.geojson')
    df["REGIAO_ADM"] = df.REGIAO_ADM.str.strip(" ").map(lambda x: unidecode.unidecode(x))
    df['REGIAO_ADM'] = df['REGIAO_ADM'].replace(['SANTA TEREZA'],'SANTA TERESA')
    df['REGIAO_ADM'] = df['REGIAO_ADM'].replace(['COMPLEXO DA MARE'],'MARE')
    df.rename(columns={ "REGIAO_ADM" : "regions" } ,inplace=True)
    adm_boundaries = df[['regions', 'geometry']]
    adm_regions = adm_boundaries.dissolve(by='regions')
    adm_regions['lat_centroid'] = adm_regions.centroid.y
    adm_regions['lon_centroid'] = adm_regions.centroid.x
    return adm_regions

def get_map_df():
    data = get_baseline_data("raw_data/preproc_data_rate.csv")
    new_model = models.load_model("/home/aklein21/code/Goldmariek/event-forecast-rio/RNN_LSTM")
    y_pred_df, baseline, actual = get_pred_actual_baseline(data, new_model, 200, 31)
    list_data = [y_pred_df, actual]
    for data in list_data:
        data = append_dates(data)
    map_df = get_folium_dataframe(y_pred_df, actual)
    map_df_hover = get_hover_text(map_df)
    df_3 = create_html_files(map_df_hover)
    adm_regions = get_shapes_centroids("raw_data/Limite_Bairro.geojson")
    df_final=df_3.merge(adm_regions, on='regions', how='left')
    return df_final
