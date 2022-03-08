import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import geopandas as gpd
import folium
import streamlit.components.v1 as components
import branca

df_final = pd.read_csv("map_df.csv")

"# streamlit-folium"

with st.echo():
    # import streamlit as st
    # from streamlit_folium import folium_static
    # import folium

    location = df_final['lat_centroid'].mean(), df_final['lon_centroid'].mean()
    m = folium.Map(location=location,zoom_start=10)

    # for _, r in df_final.iterrows():
    #     # Without simplifying the representation of each borough,
    #     # the map might not be displayed
    #     sim_geo = gpd.GeoSeries(r['geometry']) #.simplify(tolerance=0.001)
    #     geo_j = sim_geo.to_json()
    #     print(geo_j)
    #     geo_j = folium.GeoJson(data=geo_j,
    #                         style_function=lambda x: {'fillColor': 'blue'})
    #     folium.Popup(r['regions']).add_to(geo_j)
    #     geo_j.add_to(m)

    # for i in range(0,30):
    #     html=f'<iframe src="/html/fig{i}.html" width="850" height="400"  frameborder="0">'
    #     print(html)

    #     popup = folium.Popup(folium.Html(html, script=True))
    #     folium.Marker([df_final['lat_centroid'].iloc[i], df_final['lon_centroid'].iloc[i]], popup=popup,icon=folium.Icon()).add_to(m)

    ########Test 1
    #HtmlFile = open("html/fig0.html", 'r', encoding='utf-8')
    # returns "_io.TextIOWrapper name='html/fig0.html' mode='r' encoding='utf-8'>" in the popup

    ########Test 2
    # HtmlFile = folium.Html('html/fig0.html', script=True)
    # returns empty popup

    ########Test 3
    # html=f'<iframe src="fig0.html" width="850" height="400"  frameborder="0">'
    # # iframe = folium.element.IFrame(html=html, width=500, height=300)
    # popup = folium.Popup(folium.Html(html, script=True))
    # # returns "Folium has no attribute element"

    ########Test 4
    #html = f'<iframe src="/html/fig0.html" width="850" height="400"  frameborder="0">'
    # iframe = branca.element.IFrame(html=html, width=500, height=300)
    # popup = folium.Popup(iframe, max_width=2650)
    # showing empty field


    ########Test 5
    #HtmlFile = open("html/fig_11.html","r", encoding='utf-8')
    #source_code = HtmlFile.read()
    #popup = folium.Popup(source_code, max_width=3500)

    #HtmlFile = open(f"https://storage.googleapis.com/event-prediction-rio/fig0.html", "r", encoding='utf-8')
    #source_code = HtmlFile.read()

    #components.iframe("https://storage.googleapis.com/event-prediction-rio/fig0.html")

    #popup = folium.Popup("https://storage.googleapis.com/event-prediction-rio/fig0.html", parse_html=True, max_width=6000)

    #html= f'<iframe src={"html/fig_11.html"} width="850" height="400" frameborder="0">'
    #popup = folium.Popup(folium.Html(html, script=True))

    #popup = folium.Popup(components.html(source_code), max_width=3500)

    # source_code = HtmlFile.read()
    # test = folium.Html('html/fig0.html', script=True)
    # popup = folium.Popup(test, max_width=2650)
    # iframe = branca.element.IFrame(html=HtmlFile,width=510,height=280)

    #folium.Marker([df_final['lat_centroid'].iloc[0], df_final['lon_centroid'].iloc[0]], popup=popup,icon=folium.Icon()).add_to(m)

    # source_code = HtmlFile.read()
    # components.html(source_code)

    HtmlFile = open("index.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=800, height=800)



    # call to render Folium map in Streamlit
    folium_static(m)
