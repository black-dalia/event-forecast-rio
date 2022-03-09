import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import geopandas as gpd
import folium
import streamlit.components.v1 as components
import requests
# from multipage import MultiPage


# app = MultiPage()

df_final = pd.read_csv("map_df.csv")

st.markdown("""
            Crime prediction for Rio de Janeiro

            ###### Below you can find predicted number of crimes for January 2020 for administrative regions of Rio de Janeiro.
            ###### Click on the desired region and see predicted values as well as actual values from 2018 - 2019.

    """)

# Create a page dropdown
page = st.selectbox("Navigation", ["Get crime predictions", "Learn more about our project", "Get news from Polícia Civil RJ"])
if page == "Get crime predictions":
    # Display details of page 1

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
# folium_static(m)


elif page == "Learn more about our project":
    # Display details of page 2

    st.markdown("""
            Lorem ipsum sit dolor...

    """)

elif page == "Get news from Polícia Civil RJ":
    # Display details of page 3

    st.markdown("""
            Crime prediction for Rio de Janeiro

            ###### Below you can find predicted number of crimes for January 2020 for administrative regions of Rio de Janeiro.
            ###### Click on the desired region and see predicted values as well as actual values from 2018 - 2019.

    """)

    class Tweet(object):
        def __init__(self, s, embed_str=False):
            if not embed_str:
                # Use Twitter's oEmbed API
                # https://dev.twitter.com/web/embedded-tweets
                api = "https://publish.twitter.com/oembed?url={}".format(s)
                response = requests.get(api)
                self.text = response.json()["html"]
            else:
                self.text = s

        def _repr_html_(self):
            return self.text

        def component(self):
            return components.html(self.text, height=600)


    t = Tweet("https://twitter.com/pcerj?lang=en").component()


    # def theTweet(tweet_url):
    #     api = "https://publish.twitter.com/oembed?url".format(tweet_url)
    #     response = requests.get(api)
    #     res = response.json()
    #     return res

    # res = theTweet("https://twitter.com/PCERJ?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor")
    # st.write(res)

# with st.echo():
#     # import streamlit as st
#     # from streamlit_folium import folium_static
#     # import folium
